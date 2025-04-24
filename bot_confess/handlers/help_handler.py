from aiogram import Router, types
from aiogram.filters import Command

help_router = Router()

@help_router.message(Command("help"))
async def help_handler(message: types.Message):
    print("helper terpanggil!!")
    await message.answer("""
                         
Untuk mengirim confess
1. Ketik /confess
2. Kirim username penerima confess
3. Kirim pesan confess
                         
                         """)