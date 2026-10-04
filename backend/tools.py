from pathlib import Path
import json
import sqlite3
from typing import Any
from models import AlternativeProduct, AlternativesResult, ProductInfo, StockLine, StockLookup
from audit import audit_event

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "data" / "campus_customs.db"

def _find_product(conn: sqlite3.Connection, query: str) -> sqlite3.Row | None:
    exact = conn.execute("SELECT * FROM catalogue WHERE product_id = ? OR lower(name) = lower(?)", (query, query)).fetchone()
    if exact:
        return exact
    return conn.execute("SELECT * FROM catalogue WHERE lower(name) LIKE lower(?) ORDER BY name LIMIT 1", (f"%{query}%",)).fetchone()

def get_product_info(product: str) -> ProductInfo:
    """Return factual catalogue fields for one product, or unknown_product when it is absent."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        row = _find_product(conn, product.strip())
        if row is None:
            result = ProductInfo(status="unknown_product")
        else:
            result = ProductInfo(status="found", product_id=row["product_id"], name=row["name"], description=row["description"], garment_type=row["garment_type"], price=row["price"], colors=json.loads(row["colors"]), image_file_path=row["image_file_path"])
        audit_event("product_information", {"product": product}, result.status, "tool completed")
        return result
    finally:
        conn.close()

def get_stock(product: str, size: str | None = None) -> StockLookup:
    """Look up all or size-specific inventory without inventing missing stock."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        row = _find_product(conn, product.strip())
        if row is None:
            result = StockLookup(status="unknown_product", requested_size=size)
            audit_event("inventory_lookup", {"product": product, "size": size}, result.status, "tool completed")
            return result
        rows = conn.execute("SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY id", (row["product_id"],)).fetchall()
        stock = [StockLine(size=item["size"], quantity=item["quantity"]) for item in rows]
        if size is None:
            result = StockLookup(status="in_stock" if any(item.quantity > 0 for item in stock) else "out_of_stock", product_id=row["product_id"], product_name=row["name"], stock=stock)
            audit_event("inventory_lookup", {"product": product, "size": size}, result.status, "tool completed")
            return result
        match = next((item for item in stock if item.size.lower() == size.strip().lower()), None)
        if match is None:
            result = StockLookup(status="unavailable_size", product_id=row["product_id"], product_name=row["name"], requested_size=size, stock=stock)
        else:
            result = StockLookup(status="in_stock" if match.quantity > 0 else "out_of_stock", product_id=row["product_id"], product_name=row["name"], requested_size=match.size, stock=stock, quantity=match.quantity)
        audit_event("inventory_lookup", {"product": product, "size": size}, result.status, "tool completed")
        return result
    finally:
        conn.close()

def search_catalogue(query: str, limit: int = 8) -> list[dict[str, Any]]:
    aliases = {"sweatshirt": "hoodie", "sweatshirts": "hoodie", "hoodies": "hoodie", "tee": "tshirt", "tees": "tshirt", "jumper": "sweater", "jumpers": "sweater"}
    terms = [aliases.get(term.lower().rstrip("s"), term.lower().rstrip("s")) for term in query.split() if len(term) > 2]
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT * FROM catalogue ORDER BY name").fetchall()
        scored = []
        for row in rows:
            haystack = " ".join([row["name"], row["garment_type"], row["description"], row["colors"], row["search_tags"]]).lower()
            score = sum(term in haystack for term in terms)
            if score:
                inventory = [dict(item) for item in conn.execute("SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY id", (row["product_id"],))]
                scored.append((score, row, inventory))
        scored.sort(key=lambda item: (-item[0], item[1]["name"]))
        result = [{"product_id": row["product_id"], "name": row["name"], "garment_type": row["garment_type"], "description": row["description"], "colors": json.loads(row["colors"]), "price": row["price"], "image_url": f"/media/{row['image_file_path']}", "inventory": inventory} for _, row, inventory in scored[:limit]]
        audit_event("catalogue_search", {"query": query, "limit": limit}, {"count": len(result)}, "tool completed")
        return result
    finally:
        conn.close()

def alternative_products(product: str, limit: int = 4) -> AlternativesResult:
    """Find database-backed alternatives using garment type, colors, and search tags."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        source = _find_product(conn, product.strip())
        if source is None:
            result = AlternativesResult(status="unknown_product", source_product=product)
            audit_event("alternatives_for_unavailable", {"product": product, "limit": limit}, result.status, "tool completed")
            return result
        source_colors = set(json.loads(source["colors"]))
        source_tags = set(json.loads(source["search_tags"]))
        candidates = []
        for row in conn.execute("SELECT * FROM catalogue WHERE product_id != ?", (source["product_id"],)):
            colors = set(json.loads(row["colors"]))
            tags = set(json.loads(row["search_tags"]))
            same_type = row["garment_type"] == source["garment_type"]
            overlap = len(source_colors & colors) + len(source_tags & tags)
            score = (5 if same_type else 0) + overlap
            if score:
                reason = "same garment type" if same_type else "shared colors or search tags"
                candidates.append((score, row, reason))
        candidates.sort(key=lambda item: (-item[0], item[1]["name"]))
        result = AlternativesResult(status="found", source_product=source["name"], alternatives=[AlternativeProduct(product_id=row["product_id"], name=row["name"], price=row["price"], image_url=f"/media/{row['image_file_path']}", reason=reason) for _, row, reason in candidates[:limit]])
        audit_event("alternatives_for_unavailable", {"product": product, "limit": limit}, {"status": result.status, "count": len(result.alternatives)}, "tool completed")
        return result
    finally:
        conn.close()
