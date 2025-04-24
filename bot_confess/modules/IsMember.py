from aiogram import Bot
from aiogram.types import Message

# Pakai ID (integer), misal -100xxxxxxxxx
CHANNEL_IDS = [-1002618820502]

async def is_member(bot: Bot, message: Message) -> bool:
    user_id = message.from_user.id
    not_subscribed = []

    for channel_id in CHANNEL_IDS: # Ambil channel_id dari CHANNEL_IDS
        try:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status in ('left', 'kicked'):
                not_subscribed.append(channel_id)
        except Exception as e:
            not_subscribed.append(channel_id)

    if not_subscribed:
        text = "❗Untuk menggunakan bot ini, kamu harus join channel berikut:\n\n"
        for ch in not_subscribed:
            try:
                channel = await bot.get_chat(ch) # Ubah ID menjadi Username 
                text += f"@{channel.username}, "
            except Exception as e:
                text += f"{ch}, "
        text += "\nSetelah join, silakan kirim /start lagi."
        await message.answer(text)
        return False

    return True
