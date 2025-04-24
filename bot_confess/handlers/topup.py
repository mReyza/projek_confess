from aiogram import Router, types
from aiogram.filters import Command

topup_router = Router()

@topup_router.message(Command("topup"))
async def help_handler(message: types.Message):
    print("support terpanggil")
    await message.answer("""
🪙 Ingin Top Up Koin?

Silakan hubungi Admin : @Reyy_03 atau @croduct

📦 Daftar Paket Koin:
• 3 Koin  —  500 Rp
• 7 Koin  —  1.000 Rp
• 12 Koin —  1.500 Rp
info lebih lanjut hub admin

✨ Koin dapat digunakan untuk mengirim confess
                         """)