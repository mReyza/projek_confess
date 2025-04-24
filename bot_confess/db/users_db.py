import sqlite3
from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from config.config_db import main_path


def init_db():
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    
    # Tabel users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabel pending menfess
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_menfess (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            channel_username TEXT,
            owner_username TEXT,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabel notifikasi pemilik channel
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channel_owner_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_username TEXT,
            owner_username TEXT,
            message TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def save_user(user_id: int):
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()


def get_user(user_id: int):
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_user_balance(user_id: int, amount: int):
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()


def get_user_balance(user_id: int):
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def get_count_users():
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def save_pending_menfess(user_id: int, channel_username: str, owner_username: str, message: str):
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pending_menfess (user_id, channel_username, owner_username, message)
        VALUES (?, ?, ?, ?)
    """, (user_id, channel_username, owner_username, message))
    conn.commit()
    conn.close()


def notify_channel_owner(channel_username: str, owner_username: str, message: str):
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO channel_owner_notifications (channel_username, owner_username, message)
        VALUES (?, ?, ?)
    """, (channel_username, owner_username, message))
    conn.commit()
    conn.close()


class UserSaverMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.message:
            user_id = event.message.from_user.id
            save_user(user_id)
        return await handler(event, data)
