import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from db.users_db import get_count_users

admin_router = Router()

@admin_router.message(Command("stats"))
async def statistik_sederhana(message: types.Message):
    print(f"penggunaan command admin : {message.from_user.full_name} ")
    count = get_count_users()
    await message.answer(f"""

TOTAL USERS {count}

                         """)