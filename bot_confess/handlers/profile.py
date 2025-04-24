from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from db.helpers import fetch_one

router = Router()

@router.message(Command("profile"))
async def profile(message: Message):
    user_id = message.from_user.id

    # Ganti `id` jadi `user_id` dan `?` jadi `$1` (untuk PostgreSQL)
    user = await fetch_one("SELECT coin FROM users WHERE user_id = $1", user_id)

    if not user:
        await message.answer("🔍 Data tidak ditemukan. Kamu belum terdaftar di sistem.")
        return

    coin = user["coin"]  # Bisa juga user[0] jika fetchrow biasa

    await message.answer(f"""
📜 Informasi Pengguna                         
                         
👤 ID Anda: {user_id}

🪙 Coin yang Anda miliki: {coin}

✨ Gunakan koin Anda untuk mengirim confess.
    """)
