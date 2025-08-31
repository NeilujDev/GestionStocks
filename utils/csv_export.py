from typing import Optional
import csv
from repo.movement_repository import list_movements


def export_movements_csv(path: str, article_id: Optional[int] = None) -> int:
    """Exporte les mouvements en CSV (UTF-8 BOM pour Excel). Retourne le nb de lignes écrites."""
    rows = list_movements(article_id=article_id, limit=10_000_000)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "article_id", "kind", "quantity", "created_at"])
        for r in rows:
            w.writerow(r)
    return len(rows)
