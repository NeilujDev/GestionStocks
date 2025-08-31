from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Article:
    id: int | None
    name: str
    description: str = ""


@dataclass(frozen=True)
class Movement:
    id: int | None
    article_id: int
    kind: str  # "IN" ou "OUT"
    quantity: int
    created_at: datetime
