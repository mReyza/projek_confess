from config.config_ids import LOG_CHANNEL_ID
import asyncio
from aiogram import types

async def send_log_message(message: types.Message, receiver_id: int):
    receiver = await message.bot.get_chat(receiver_id)

    # Handle pengirim
    if message.from_user.username:
        sender_display = f"@{message.from_user.username}"
    else:
        sender_display = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a>'

    # Handle penerima
    if receiver.username:
        receiver_display = f"@{receiver.username}"
    else:
        receiver_display = f'<a href="tg://user?id={receiver.id}">{receiver.full_name}</a>'

    logs_text = f"""
Dari: {sender_display}
Ke: {receiver_display}
Pesan:
{message.html_text}
    """
    await message.bot.send_message(LOG_CHANNEL_ID, logs_text, parse_mode="HTML")
