# config/config_db.py
from pathlib import Path

# Folder config
base_dir = Path(__file__).resolve().parent

main_path = base_dir / "main.db"
pending_confess_path = base_dir / "pending_confess.db"