# Campus Customs — HW 4

Campus Customs is a React/Vite storefront backed by FastAPI, SQLite, and a PydanticAI shop assistant.

## Submission layout

- `frontend/` — React, TypeScript, and CSS storefront
- `backend/` — FastAPI app, PydanticAI agent, database tools, prompt, and audit helper
- `output/` — harness and usability/design documentation plus audit output

The local data pack is intentionally excluded from Git. Place the supplied archive in the project root and unpack it so the database is available at `data/data/campus_customs.db` and original images are available at `data/data/products/`.

## Configuration

Copy `.env.example` to `.env` in the repository root and set `PORTKEY_API_KEY` locally. Keep the real `.env` private. The default model is `gpt-5.6-luna`; `OPENAI_MODEL` may override it locally.

## Backend

```powershell
cd backend
..\.venv\Scripts\python.exe -m pip install -r ..\requirements.txt
  ..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8015
```

The backend reads the existing SQLite schema; no destructive initialization is required. If starting from a fresh data pack, unpack it as described above. Existing password-format migration is performed safely when the known test account logs in.

## Frontend

In a second terminal:

```powershell
npm install
npm run dev
```

For a repeatable local launch after reopening VS Code, from `hw4` run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\start_hw4.ps1
```

Then open `http://127.0.0.1:5175/`. The script starts the backend on port 8015 and connects the Vite frontend to it.

Open the Vite URL shown in the terminal. If the backend uses another port, set `VITE_API_URL` before starting Vite.

## Verification

```powershell
npm run build
```

The app uses real catalogue and inventory data, session-scoped chat history, structured agent tools, and an append-only `output/audit_trail.json`. Problem 11 evidence is in `output/app_check.html` with screenshots in `output/app_check_images/`.

The public submission repository is https://github.com/DanielKim-94/hw4.
