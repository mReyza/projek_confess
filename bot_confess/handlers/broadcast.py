import sqlite3

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command
from aiogram.types import Message

from config.config_db import main_path

router = Router()

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    print(f"penggunaan command admin user name : {message.from_user.full_name}  pesan : {message.text}")
    if len(message.text.split(" ", 1)) < 2:
        await message.answer("❗ Format salah.\nGunakan: `/broadcast isi pesan`", parse_mode="Markdown")
        return

    broadcast_text = message.text.split(" ", 1)[1]

    # Ambil user dari DB
    conn = sqlite3.connect(main_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()

    success = 0
    failed = 0

    for (user_id,) in users:
        try:
            await message.bot.send_message(user_id, broadcast_text)
            success += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1

    await message.answer(f"📢 Broadcast selesai!\n✅ Berhasil: {success}\n❌ Gagal: {failed}")