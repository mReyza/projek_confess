from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.config_admin import ADMIN_ID
from db.users_db import update_user_balance

admin1_router = Router()
admin_state = {}

@admin1_router.message(Command("coin"))
async def cmd_coin_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Kamu tidak punya izin untuk perintah ini.")
        return

    await message.answer("Kirimkan @username pengguna yang ingin kamu beri coin.")
    admin_state[message.from_user.id] = {"step": "awaiting_username"}

@admin1_router.message()
async def handle_admin_input(message: Message):
    user_id = message.from_user.id
    if user_id not in admin_state:
        return

    step = admin_state[user_id]["step"]

    if step == "awaiting_username":
        username = message.text.strip().lstrip("@")
        admin_state[user_id]["username"] = username
        admin_state[user_id]["step"] = "awaiting_coin"
        await message.answer(f"Berapa coin yang ingin diberikan ke @{username}?")

    elif step == "awaiting_coin":
        try:
            amount = int(message.text.strip())
            username = admin_state[user_id]["username"]
            update_user_balance(username, amount, by_username=True)
            await message.answer(f"Berhasil menambahkan {amount} coin ke @{username}.")
        except ValueError:
            await message.answer("Jumlah coin harus angka.")
        admin_state.pop(user_id)
