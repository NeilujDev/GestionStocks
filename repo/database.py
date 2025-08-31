import sqlite3
from pathlib import Path

DB_PATH = Path("stock.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_schema() -> None:
    with get_connection() as conn:
        conn.executescript(
            """
        CREATE TABLE IF NOT EXISTS articles(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT DEFAULT ""
        );
        CREATE TABLE IF NOT EXISTS movements(
            id INTEGER PRIMARY KEY,
            article_id INTEGER NOT NULL,
            kind TEXT NOT NULL CHECK(kind IN ('IN','OUT')),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(article_id) REFERENCES articles(id)
        );
        """
        )
