from pathlib import Path
import json
import sqlite3
import base64
import hashlib
import hmac
import secrets
from urllib.parse import urlparse
from typing import Any

from fastapi import Cookie, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from agent import run_chat
from models import ChatRequest, ChatResponse, CustomerContext

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "data" / "campus_customs.db"
IMAGE_ROOT = ROOT / "data" / "data"

app = FastAPI(title="Campus Customs API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory=IMAGE_ROOT), name="media")
PASSWORD_ITERATIONS = 310_000
SESSIONS: dict[str, int] = {}

class Registration(BaseModel):
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class Login(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

def hash_password(password: str) -> str:
    salt = secrets.token_urlsafe(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PASSWORD_ITERATIONS)
    encoded = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return f"pbkdf2_sha256${PASSWORD_ITERATIONS}${salt}${encoded}"

def verify_password(password: str, stored: str) -> tuple[bool, bool]:
    parts = stored.split("$")
    if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
        return False, False
    try:
        iterations, salt, expected = int(parts[1]), parts[2], parts[3]
        actual = base64.urlsafe_b64encode(hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations)).decode().rstrip("=")
        return hmac.compare_digest(actual, expected), iterations != PASSWORD_ITERATIONS
    except (ValueError, TypeError):
        return False, False

def public_user(row: sqlite3.Row) -> dict[str, Any]:
    return {"id": row["id"], "first_name": row["first_name"], "last_name": row["last_name"], "name": row["name"], "email": row["email"]}

def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = user_id
    return token

def session_user(token: str | None, conn: sqlite3.Connection) -> sqlite3.Row | None:
    user_id = SESSIONS.get(token or "")
    return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone() if user_id else None


def product_from_row(row: sqlite3.Row, conn: sqlite3.Connection) -> dict[str, Any]:
    inventory = conn.execute(
        "SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY id",
        (row["product_id"],),
    ).fetchall()
    return {
        "product_id": row["product_id"],
        "name": row["name"],
        "garment_type": row["garment_type"],
        "description": row["description"],
        "colors": json.loads(row["colors"]),
        "search_tags": json.loads(row["search_tags"]),
        "image_file_path": row["image_file_path"],
        "image_url": f"/media/{row['image_file_path']}",
        "price": row["price"],
        "inventory": [dict(item) for item in inventory],
    }


def get_connection() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Database not found: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/api/auth/register")
def register(payload: Registration) -> dict[str, Any]:
    conn = get_connection()
    try:
        email = str(payload.email).lower()
        if conn.execute("SELECT 1 FROM users WHERE lower(email) = ?", (email,)).fetchone():
            raise HTTPException(status_code=409, detail="An account with this email already exists.")
        cur = conn.execute("INSERT INTO users (name, email, password_hash, first_name, last_name) VALUES (?, ?, ?, ?, ?)", (f"{payload.first_name} {payload.last_name}", email, hash_password(payload.password), payload.first_name, payload.last_name))
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
        return {"user": public_user(row), "session_token": create_session(row["id"]), "message": "Account created successfully."}
    finally:
        conn.close()

@app.post("/api/auth/login")
def login(payload: Login) -> dict[str, Any]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE lower(email) = ?", (str(payload.email).lower(),)).fetchone()
        if row is None:
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        valid, needs_migration = verify_password(payload.password, row["password_hash"])
        if not valid:
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        if needs_migration:
            conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (hash_password(payload.password), row["id"]))
            conn.commit()
        return {"user": public_user(row), "session_token": create_session(row["id"]), "message": "Logged in successfully."}
    finally:
        conn.close()


@app.get("/api/products")
def products() -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM catalogue ORDER BY name").fetchall()
        return [product_from_row(row, conn) for row in rows]
    finally:
        conn.close()

@app.get("/api/chat/history")
def chat_history(x_session_token: str | None = Header(default=None), campus_session: str | None = Cookie(default=None)) -> list[dict[str, Any]]:
    conn = get_connection()
    try:
        user = session_user(x_session_token or campus_session, conn)
        if user is None:
            raise HTTPException(status_code=401, detail="Login required to load chat history.")
        rows = conn.execute("SELECT role, content, created_at FROM chat_messages WHERE user_id = ? ORDER BY id", (user["id"],)).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, x_session_token: str | None = Header(default=None), campus_session: str | None = Cookie(default=None), referer: str | None = Header(default=None)) -> ChatResponse:
    conn = get_connection()
    try:
        user = session_user(x_session_token or campus_session, conn)
        history = payload.conversation
        page = payload.current_page
        product_id = payload.product_id
        if referer:
            ref_path = urlparse(referer).path
            page = page or ref_path
            product_id = product_id or (ref_path.split("/products/", 1)[1] if "/products/" in ref_path else None)
        customer = CustomerContext(current_page=page, product_id=product_id)
        if user:
            customer.user_id, customer.name, customer.email = user["id"], user["name"], user["email"]
            stored = conn.execute("SELECT role, content FROM chat_messages WHERE user_id = ? ORDER BY id DESC LIMIT 8", (user["id"],)).fetchall()
            history = [dict(row) for row in reversed(stored)]
        if product_id:
            row = conn.execute("SELECT * FROM catalogue WHERE product_id = ?", (product_id,)).fetchone()
            if row:
                customer.current_product = product_from_row(row, conn)
        answer = run_chat(payload.message, history, customer)
        if user:
            conn.execute("INSERT INTO chat_messages (user_id, role, content, products_json) VALUES (?, 'user', ?, NULL)", (user["id"], payload.message))
            conn.execute("INSERT INTO chat_messages (user_id, role, content, products_json) VALUES (?, 'assistant', ?, ?)", (user["id"], answer.message, json.dumps([item.model_dump() for item in answer.suggested_products])))
            conn.commit()
        return answer
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        conn.close()


@app.get("/api/products/{product_id}")
def product(product_id: str) -> dict[str, Any]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM catalogue WHERE product_id = ?", (product_id,)
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product_from_row(row, conn)
    finally:
        conn.close()
