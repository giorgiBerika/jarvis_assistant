import sqlite3 
from pathlib import Path 
from datetime import datetime, timezone 


DB_PATH = Path(__file__).parent.parent / "memory.db"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    
    """)

    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            ts TEXT NOT NULL
        )
    """)

    return conn 


def remember_fact(key: str, value: str) -> str:
    conn = _connect()
    conn.execute(
        "INSERT INTO facts (key, value, updated_at) VALUES (?, ?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
        (key, value, datetime.now(timezone.utc).isoformat()),

    )
    conn.commit()
    conn.close()

    return "Fact saved!"


def recall_facts() -> dict[str, str]:
    conn = _connect()
    rows = conn.execute(
        "SELECT key, value FROM facts"
    ).fetchall()
    conn.close()
    return dict(rows)


def log_message(role: str, content: str) -> None:
    conn = _connect()
    conn.execute(
        "INSERT INTO messages (role, content, ts) VALUES (?, ?, ?)",
        (role, content, datetime.now(timezone.utc).isoformat()), 
    )
    conn.commit()
    conn.close()



def recent_messages(limit: int = 10 ) -> list[dict]:
    conn = _connect()
    rows = conn.execute(
        "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]


