from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_DIR = BASE_DIR / "storage"
FILES_DIR = STORAGE_DIR / "files"
DATA_FILE = STORAGE_DIR / "database.db"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
FILES_DIR.mkdir(parents=True, exist_ok=True)
