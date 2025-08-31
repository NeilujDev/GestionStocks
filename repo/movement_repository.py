from typing import Optional, List, Tuple
import sqlite3
from .database import get_connection


def get_stock(article_id: int) -> int:
    """Stock courant = IN - OUT pour un article."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
              COALESCE(SUM(CASE WHEN kind='IN'  THEN quantity END),0) -
              COALESCE(SUM(CASE WHEN kind='OUT' THEN quantity END),0)
            FROM movements
            WHERE article_id=?;
        """,
            (article_id,),
        ).fetchone()
        return int(row[0] or 0)


def create_movement(article_id: int, kind: str, quantity: int) -> int:
    """Crée un mouvement IN/OUT. Lève sqlite3.IntegrityError si stock insuffisant."""
    kind = kind.upper().strip()
    if kind not in ("IN", "OUT"):
        raise ValueError("kind doit être 'IN' ou 'OUT'.")
    if quantity <= 0:
        raise ValueError("La quantité doit être > 0.")

    with get_connection() as conn:
        try:
            cur = conn.execute(
                "INSERT INTO movements(article_id, kind, quantity) VALUES (?, ?, ?);",
                (article_id, kind, quantity),
            )
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            # Repack message clair pour l'UI
            msg = str(e)
            if "Stock insuffisant" in msg:
                raise ValueError("Stock insuffisant pour effectuer la sortie.") from e
            if "FOREIGN KEY" in msg:
                raise ValueError("Article inexistant.") from e
            if "CHECK" in msg:
                raise ValueError("Données invalides pour le mouvement.") from e
            raise


def list_movements(article_id: Optional[int] = None, limit: int = 100) -> List[Tuple]:
    """Liste des mouvements (id, article_id, kind, quantity, created_at)."""
    with get_connection() as conn:
        if article_id is None:
            rows = conn.execute(
                """
                SELECT id, article_id, kind, quantity, created_at
                FROM movements ORDER BY datetime(created_at) DESC LIMIT ?;
            """,
                (limit,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, article_id, kind, quantity, created_at
                FROM movements
                WHERE article_id=? ORDER BY datetime(created_at) DESC LIMIT ?;
            """,
                (article_id, limit),
            ).fetchall()
        return rows
