import logging
import re
import sqlite3

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from modules.IsMember import is_member
from modules.Logs_Confess import send_log_message
from userbot.modules.get_chat_id import get_user_id_telethon, send_message
from db.users_db import (get_user_balance, save_pending_menfess,
                                 update_user_balance)
from db.users_db import notify_channel_owner

confess_router = Router()
cancel_router = Router()
             
def button_reply(receiver_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Reply", callback_data=f"reply_to_reciever:{receiver_id}")
    return keyboard.as_markup()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot_log.txt", encoding="utf-8", mode='w'),
        logging.StreamHandler()
    ]
)

KATA_KASAR = [
    "kontol", "kontl", "kntl", "ktl", "memek", "momok", "mmk",
    "memk", "pepek", "ppek", "goblok", "gblk", "bangsat", "bgst",
    "tai", "mmok", "taik", "ajg", "anjing", "babi", "monyet", "setan", "iblis",
    "sial", "bodoh", "bngng", "cilaka", "laknat", "bool",
    "baka", "kusotare", "kutabare", "shine", "shabi", "cao ni ma", "gou ri de",
    "gaesaekki", "byeongshin", "jot", "ssibal", "blyat", "pidaras",
    "cabron", "pendejo", "hijo de puta", "connard", "merde", "pute","arschloch",
    "scheisse", "fuck", "shit", "bitch", "asshole", "bastard", "cunt", "dick",
    "fck", "fuk", "sh1t", "b1tch", "bstrd", "cnt", "d1ck"
]

# States
class Form(StatesGroup):
    username = State()
    message = State()

@confess_router.message(Command("confess"))
async def cmd_start(message: types.Message, state: FSMContext):
    member = await is_member(message.bot, message)
    print(f"memulai confess username : {message.from_user.full_name}")
    await message.answer("Halo! Masukkan username Telegram penerima (format: @username):")
    await state.set_state(Form.username)

@confess_router.message(Form.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    if not username.startswith("@"):
        await message.answer('''
⚠️ Username harus dimulai dengan @. 

Contoh : @username
Dan username harus benar!                    
        ''')
        return
    
    await state.update_data(username=username[1:])
    await message.answer("Sekarang tuliskan pesan yang ingin Anda kirim:")
    await state.set_state(Form.message)

def save_failed_message(receiver_id, sender_id, message_text):
    conn = sqlite3.connect(pending_confess_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_confess (
            receiver_id INTEGER NOT NULL,
            sender_id TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    
    cursor.execute("INSERT INTO pending_confess (receiver_id, sender_id, message) VALUES (?, ?, ?)", (receiver_id, sender_id, message_text))
    conn.commit()
    conn.close()

@confess_router.message(Form.message)
async def process_message(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get('username')
    msg_text = message.text
    sender_id = message.chat.id
    
    try:
        # Get user info by username using aiogram's get_chat
        receiver_id = await get_user_id_telethon(username)
        print(f"Receiver ID: {receiver_id}  {message.text}")
        
    except Exception as e:
        logging.error(f"Error getting user info: {e}")
        await message.answer(f"⚠️ Gagal menemukan pengguna dengan username @{username}. Pastikan username benar.")
        await state.clear()
        return
    
    # Check for bad words
    if any(re.search(rf"\b{word}\b", msg_text, re.IGNORECASE) for word in KATA_KASAR):
        await message.answer("⚠️ Pesan Anda mengandung kata yang tidak diperbolehkan! Silakan kirim ulang tanpa kata kasar, Dan jangan mengulanginya lagi!!")
        return

    try:
        # Send the message
        await message.bot.send_message(
            chat_id=receiver_id,
            text=f"💌 Wahh.. Ada yang confess ke kamu nih!\n\nPesan: {msg_text}",
            reply_markup=button_reply(sender_id)
        )
        await send_log_message(message, receiver_id)
        await message.answer("✅ Confess kamu berhasil dikirim!")
    
    except Exception as e:
        logging.error(f"❌ Gagal mengirim pesan ke @{username}: {e}")
        save_failed_message(receiver_id, message.from_user.id, msg_text)  # Simpan pesan yang gagal
        await send_message(f"Seseorang mengirimmu confess! \n\n<blockquote>{msg_text}</blockquote>\n\n ingin membalas confess ini? @anonymous_confess_bot, tekan dan reply!", username)
        await message.answer("⚠️ Pesan mu tersimpan!, Pastikan username yang kamu tuju sudah chat bot.")

    await state.clear()

@cancel_router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Confess dibatalkan.")