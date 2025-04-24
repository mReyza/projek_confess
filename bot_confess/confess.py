import asyncio
import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from config.config_bot import TOKEN
from db import init_db
from db.users_db import UserSaverMiddleware
from handlers import all_routers


# Fungsi untuk menetapkan perintah menggunakan `SetMyCommands`
async def set_commands(bot):
    
    # Daftar perintah yang ingin ditetapkan
    commands = [
        BotCommand(command="start", description="memulai"),
        BotCommand(command="confess", description="confess"),
        BotCommand(command="cancel", description="Batalkan confess"),
        BotCommand(command="help", description="bantuan"),
        BotCommand(command="support", description="donasi"),
        BotCommand(command="feedback", description="laporkan masalah")
    ]
    
    # Tetapkan perintah hanya untuk obrolan pribadi
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()  # Cakupan untuk semua obrolan pribadi
    )
    print("Perintah berhasil diatur untuk semua obrolan pribadi.")
    
async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    init_db()
    
    # Register Middlewares
    dp.update.outer_middleware(UserSaverMiddleware())
    
    # Register Commands
    await set_commands(bot)
        
    # await bot.delete_webhook(drop_pending_updates=True)
    # print("✅ Webhook dihapus, semua pending updates dibuang.")
    
    # Include all routers
    for router in all_routers:
        dp.include_router(router)        
        
    # Start polling
    await dp.start_polling(bot, drop_pending_updates=True)
    

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())