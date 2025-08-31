from pathlib import Path
from datetime import datetime
from shutil import copy2
from repo.database import DB_PATH

def backup_db(target_dir: str = "exports") -> str:
    out = Path(target_dir)
    out.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Base introuvable: {DB_PATH}")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = out / f"stock-backup-{ts}.db"
    copy2(DB_PATH, dest)
    return str(dest)
