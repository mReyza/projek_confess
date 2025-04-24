from aiogram import BaseMiddleware
from db.helpers import fetch_one

async def insert_user(user_id: int) -> bool:
    result = await fetch_one(
        """
        INSERT INTO users (user_id)
        VALUES ($1)
        ON CONFLICT (user_id) DO NOTHING
        RETURNING user_id;
        """,
        user_id
    )
    return result is not None

def extract_user(event):
    # Paling umum dan langsung
    if hasattr(event, "from_user"):
        return event.from_user
    # Kasus: event.message.from_user
    if hasattr(event, "message") and hasattr(event.message, "from_user"):
        return event.message.from_user
    return None

class InsertUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = extract_user(event)
        if user:
            is_new_user = await insert_user(user.id)
            data["is_new_user"] = is_new_user

        return await handler(event, data)