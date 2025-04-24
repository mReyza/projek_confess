import sqlite3

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .reply_to_sender_handler import button_reply

start_router = Router()

def button_reply(receiver_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Reply", callback_data=f"reply_to_reciever:{receiver_id}")
    return keyboard.as_markup()

def get_pending_confess(receiver_id):
    conn = sqlite3.connect(pending_confess_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT sender_id, message FROM pending_confess WHERE receiver_id = ?", (receiver_id,))
    sender_id = cursor.fetchall()
    conn.close()
    
    return sender_id

# Fungsi untuk menghapus pesan gagal setelah ditampilkan
def delete_pending_confess(receiver_id):
    conn = sqlite3.connect(pending_confess_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pending_confess WHERE receiver_id = ?", (receiver_id,))
    conn.commit()
    conn.close()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    print(f"Handler /start terpanggil!   pemanggil : {message.from_user.full_name}")
    pending_confess = get_pending_confess(message.from_user.id)

    response = """
Halo... selamat datang di bot confess
Kalau kamu ingin memulai Click /confess

Mau confess ke siapa nihh..? Ditunggu confess-nyaa!

Ada bot bagus nihh recommended for you: https://t.me/SFSLOCK
    """

    keyboard = InlineKeyboardBuilder()

    # Kirim pesan sambutan
    await message.answer(response, reply_markup=keyboard.as_markup())

    # Jika ada pesan gagal, kirim satu per satu dengan tombol reply
    if pending_confess:
        for sender_id, msg in pending_confess:  # Langsung unpack sender_id dan pesan
            reply_kb = button_reply(sender_id)  # Kirim tombol reply dengan sender_id
            print(f"usermane: {message.from_user.full_name}")
            await message.answer(f"💌 Wahh.. Ada yang confess ke kamu nih!:\n- {msg}", reply_markup=reply_kb)
            reply_markup=button_reply(sender_id)

        # Hapus pesan gagal setelah ditampilkan
        delete_pending_confess(message.from_user.id)
