from aiogram import Router, types
from aiogram.filters import Command

feedback_router = Router()

@feedback_router.message(Command("feedback"))
async def feedback_handler(message: types.Message):
    print("feedback terpanggil!!")
    await message.answer("""
🚨 Ada masalah dengan bot?
Kami mohon maaf atas ketidaknyamanannya. Jika kamu mengalami bug, error, atau fitur yang tidak berfungsi sebagaimana mestinya, silakan laporkan kepada kami!

📩 Hubungi langsung: @Reyy_03
Tim kami akan berusaha merespons secepat mungkin dan membantu menyelesaikan kendala kamu. Terima kasih atas pengertiannya! 🙏
                         """)