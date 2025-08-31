from typing import List, Optional
from dataclasses import dataclass
import sqlite3
from .database import get_connection


@dataclass(frozen=True)
class ArticleRow:
    id: int
    name: str
    description: str


def create_article(name: str, description: str = "") -> int:
    """Crée un article et retourne son id. Lève ValueError si nom invalide ou doublon."""
    name = (name or "").strip()
    if not name:
        raise ValueError("Le nom de l'article ne peut pas être vide.")
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO articles(name, description) VALUES (?, ?);",
                (name, (description or "").strip()),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError as e:
        msg = str(e)
        if "UNIQUE constraint failed: articles.name" in msg:
            raise ValueError(f"Un article nommé « {name} » existe déjà.") from e
        raise


def list_articles() -> List[ArticleRow]:
    """Liste tous les articles, triés par nom."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, description FROM articles ORDER BY name;"
        ).fetchall()
        return [ArticleRow(id=r[0], name=r[1], description=r[2]) for r in rows]


def get_article(article_id: int) -> Optional[ArticleRow]:
    with get_connection() as conn:
        r = conn.execute(
            "SELECT id, name, description FROM articles WHERE id=?;", (article_id,)
        ).fetchone()
        return ArticleRow(id=r[0], name=r[1], description=r[2]) if r else None
