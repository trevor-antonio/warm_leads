# Buyer Intake Assistant

An AI chat widget for independent real estate agents that qualifies buyer
leads and produces a scored summary for the agent to review.

This repo is being built in small, reviewable slices. **Current state:**
a FastAPI backend with a health-check endpoint and SQLite-backed lead
storage (`POST /leads`, `GET /leads`), plus a Vite + React + TypeScript
frontend. No chat logic or LLM calls yet.

## Project structure

```
backend/            FastAPI app (Python)
  app/
    main.py          FastAPI entrypoint + routes
    config.py        Typed settings, loaded from environment variables
    db.py            SQLAlchemy engine/session (SQLite)
    models.py        ORM models (Lead)
    schemas.py       Pydantic request/response schemas
  requirements.txt
  .env.example       Template for backend/.env (not committed)

frontend/            React + TypeScript app (Vite)
  src/
  package.json

.gitignore
README.md
```

## Prerequisites

- Python 3.11+
- Node.js 20+

## Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in real values later; safe to leave blank for now
uvicorn app.main:app --reload --port 8000
```

Verify it's running:

```bash
curl http://localhost:8000/health
# {"status":"ok"}

curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","phone":"555-1234","notes":"Looking for a 3BR"}'

curl http://localhost:8000/leads
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

This starts the Vite dev server at `http://localhost:5173`.

## Notes

- The Anthropic API key is read server-side only, from `backend/.env`
  (never committed, never sent to the frontend). It isn't used yet — that
  comes with the LLM integration slice.
- `backend/.env` and `frontend/.env` are both gitignored. `backend/.env.example`
  documents the variables the backend expects.
- Leads are stored in a local SQLite file (`backend/leads.db`, gitignored
  since lead data is PII). Tables are created automatically on startup —
  there's no migration tool yet, so changing the `Lead` schema later will
  need one (e.g. Alembic) to avoid losing local data.
