from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandObject, Command

from db.table.users_db import manager_coin

from db.helpers import transactional_connection

router = Router()

@router.message(Command("addcoin"))
async def handle_addcoin(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("❌ Format salah! Gunakan: /addcoin <user_id> <jumlah_coin>")
        return

    parts = command.args.split()
    if len(parts) != 2:
        await message.answer("❌ Format salah! Gunakan: /addcoin <user_id> <jumlah_coin>")
        return

    try:
        target_user_id = int(parts[0])
        coin_amount = int(parts[1])
    except ValueError:
        await message.answer("❌ user_id dan jumlah coin harus berupa angka.")
        return

    # Operasi database
    async with transactional_connection() as conn:
        existing_user = await conn.fetchrow("SELECT coin FROM users WHERE user_id = $1", target_user_id)

        if existing_user:
            # Update coin jika user sudah ada
            await manager_coin(target_user_id, coin_amount)
            await message.answer(f"✅ Menambahkan {coin_amount} coin ke user {target_user_id} (user sudah terdaftar).")
        else:
            # Insert user baru jika belum ada
            await manager_coin(target_user_id, coin_amount)
            await message.answer(f"✅ User {target_user_id} dibuat dan diberi {coin_amount} coin.")

    # ✅ Kirim notifikasi ke user yang ditambahkan coinnya
    try:
        await message.bot.send_message(
            target_user_id,
            f"💰 {coin_amount} Coin telah diterima!"
        )
    except Exception as e:
        await message.answer(f"⚠️ Coin berhasil ditambahkan, tapi tidak bisa mengirim pesan ke user {target_user_id}.\nError: {e}")
