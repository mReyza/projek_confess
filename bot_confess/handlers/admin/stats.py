import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from db.helpers import fetch_one  # Pastikan fetch_one berfungsi sesuai kebutuhan

router = Router()

@router.message(Command("stats"))
async def statistik_sederhana(message: types.Message):
    # Query untuk menghitung total user_id dari tabel users
    query = "SELECT COUNT(user_id) FROM users"
    
    # Jalankan query menggunakan fetch_one
    result = await fetch_one(query)
    
    # Ambil nilai count dari hasil
    count = result[0] if result else 0

    await message.answer(f"""
TOTAL USERS: {count}
    """)
