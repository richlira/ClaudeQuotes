from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import random

from database import get_connection, init_db

app = FastAPI(title="ClaudeQuotes API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def health():
    return {"status": "ok", "service": "ClaudeQuotes API"}


@app.get("/quotes")
def list_quotes(
    category: str | None = Query(None, description="Filter by category"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    conn = get_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM quotes WHERE category = ? LIMIT ? OFFSET ?",
            (category, limit, offset),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM quotes LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/quotes/random")
def random_quote():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM quotes").fetchall()
    conn.close()
    if not rows:
        return {"error": "No quotes found"}
    return dict(random.choice(rows))


@app.get("/quotes/{quote_id}")
def get_quote(quote_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,)).fetchone()
    conn.close()
    if not row:
        return {"error": "Quote not found"}
    return dict(row)


@app.get("/categories")
def list_categories():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT category FROM quotes ORDER BY category").fetchall()
    conn.close()
    return [r["category"] for r in rows]
