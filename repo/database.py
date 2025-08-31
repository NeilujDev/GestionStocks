import sqlite3
from pathlib import Path

DB_PATH = Path("stock.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_schema() -> None:
    # Crée les tables si absentes + index + trigger "no negative stock"
    with get_connection() as conn:
        conn.executescript(
            """
        PRAGMA foreign_keys = ON;

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

        CREATE INDEX IF NOT EXISTS idx_movements_article ON movements(article_id);

        -- Empêche une sortie (OUT) qui ferait passer le stock < 0
        CREATE TRIGGER IF NOT EXISTS trg_no_negative_stock
        BEFORE INSERT ON movements
        WHEN NEW.kind='OUT'
          AND (
            COALESCE((
              SELECT SUM(CASE WHEN kind='IN' THEN quantity ELSE -quantity END)
              FROM movements WHERE article_id = NEW.article_id
            ), 0) < NEW.quantity
          )
        BEGIN
          SELECT RAISE(ABORT, 'Stock insuffisant');
        END;
        """
        )
