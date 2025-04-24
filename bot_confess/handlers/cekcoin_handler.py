from aiogram import Router, types
from aiogram.filters import Command
from db.users_db import get_user

cekcoin_router = Router()

@cekcoin_router.message(Command("cekcoin", prefix="/"))
async def cekcoin_command(message: types.Message):
    username = message.from_user.username
    if not username:
        await message.reply("Silakan pasang username terlebih dahulu.")
        return

    user = get_user(username)
    if user:
        await message.reply(f"Koin kamu sekarang: {user[2]}")
    else:
        await message.reply("Kamu belum terdaftar. Gunakan /start dulu.")
