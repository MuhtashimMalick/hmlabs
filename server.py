"""
HM Labs — Contact Form API
Run: uvicorn server:app --reload --port 8000
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, validator
from typing import Optional

# ── Database setup ──────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent / "hmlabs.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL,
            company     TEXT,
            role        TEXT,
            service     TEXT    NOT NULL,
            budget      TEXT,
            timeline    TEXT,
            message     TEXT    NOT NULL,
            source_page TEXT,
            created_at  TEXT    NOT NULL
        )
    """)
    con.commit()
    con.close()

init_db()

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="HM Labs API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in production
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Schema ────────────────────────────────────────────────────────────────────
class ContactPayload(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    role: Optional[str] = None
    service: str
    budget: Optional[str] = None
    timeline: Optional[str] = None
    message: str
    source_page: Optional[str] = None

    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name is required")
        return v.strip()

    @validator("message")
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Message is required")
        return v.strip()


# ── Routes ────────────────────────────────────────────────────────────────────
@app.post("/api/contact", status_code=201)
def submit_contact(payload: ContactPayload):
    now = datetime.utcnow().isoformat()
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute(
            """INSERT INTO leads
               (name, email, company, role, service, budget, timeline, message, source_page, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                payload.name, payload.email, payload.company, payload.role,
                payload.service, payload.budget, payload.timeline,
                payload.message, payload.source_page, now,
            ),
        )
        con.commit()
    finally:
        con.close()
    return {"ok": True, "message": "We've received your message and will be in touch shortly."}


@app.get("/api/leads")
def list_leads(limit: int = 50):
    """Admin endpoint — list recent leads."""
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT * FROM leads ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


@app.get("/health")
def health():
    return {"status": "ok"}


# ── Serve static files (HTML, CSS, JS) if they exist ──────────────────────────
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
