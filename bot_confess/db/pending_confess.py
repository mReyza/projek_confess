import sqlite3

from config.config_db import pending_confess_path


def init_db():
    conn = sqlite3.connect(pending_confess_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_confess (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receiver_id INTEGER,
            sender_id INTEGER,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()