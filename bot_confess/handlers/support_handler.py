from aiogram import Router, types
from aiogram.filters import Command

support_router = Router()

@support_router.message(Command("support"))
async def help_handler(message: types.Message):
    print("support terpanggil")
    await message.answer("""
Dukung Kami! ✨

Jika kamu ingin memberikan dukungan atau donasi, kamu bisa mengirimkan melalui:

💰 Dana : https://link.dana.id/minta/2vtt7319f4a

Setiap donasi yang kamu berikan sangat berarti bagi kami! Terima kasih atas dukunganmu! ❤️

                         """)