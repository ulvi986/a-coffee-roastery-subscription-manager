"""
SQLite database layer for the generated app.
Creates the schema and seeds sample data on first boot.
"""
import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv("APP_DB_PATH") or str(Path(__file__).parent.parent / "data" / "app.db")
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_items_completed ON items (completed);
"""

_SEED = """
INSERT INTO items (title, completed) VALUES
  ('Welcome to your new app 👋', 1),
  ('Create your first item', 0),
  ('Mark it complete when done', 0),
  ('Delete items you no longer need', 0);
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)  # multiple statements → executescript (execute allows only one)
    count = conn.execute("SELECT COUNT(*) AS n FROM items").fetchone()["n"]
    if count == 0:
        conn.executescript(_SEED)
    return conn


def _row_to_item(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
        "createdAt": row["created_at"],
    }


def list_items() -> list[dict]:
    conn = _connect()
    try:
        rows = conn.execute("SELECT * FROM items ORDER BY completed ASC, id DESC").fetchall()
        return [_row_to_item(r) for r in rows]
    finally:
        conn.close()


def create_item(title: str) -> dict:
    conn = _connect()
    try:
        cur = conn.execute("INSERT INTO items (title) VALUES (?)", (title,))
        conn.commit()
        row = conn.execute("SELECT * FROM items WHERE id = ?", (cur.lastrowid,)).fetchone()
        return _row_to_item(row)
    finally:
        conn.close()


def update_item(item_id: int, title: str | None = None, completed: bool | None = None) -> dict | None:
    conn = _connect()
    try:
        existing = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        if not existing:
            return None
        new_title = title if title is not None else existing["title"]
        if completed is True:
            new_completed = 1
        elif completed is False:
            new_completed = 0
        else:
            new_completed = existing["completed"]
        conn.execute("UPDATE items SET title = ?, completed = ? WHERE id = ?", (new_title, new_completed, item_id))
        conn.commit()
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return _row_to_item(row)
    finally:
        conn.close()


def delete_item(item_id: int) -> bool:
    conn = _connect()
    try:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
