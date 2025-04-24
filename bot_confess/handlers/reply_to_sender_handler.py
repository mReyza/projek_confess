import logging

from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from modules.Logs_Confess import send_log_message

reply_to_sender_router = Router()

# State untuk menangkap balasan pengguna
class ReplyState(StatesGroup):
    waiting_for_reply = State()

def button_reply(receiver_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Reply", callback_data=f"reply_to_reciever:{receiver_id}")
    return keyboard.as_markup()

# Callback Query Handler untuk tombol balas
@reply_to_sender_router.callback_query(F.data.startswith("reply_to_sender:"))
async def handle_reply_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        sender_id = callback.data.split(":")[1]  # Ambil sender_id dari callback_data
        
        # Simpan sender_id di FSM untuk dikaitkan dengan pesan balasan
        await state.update_data(sender_id=sender_id)
        await callback.answer()

        await callback.answer("✏️ Ketik pesan balasan Anda:")
        await state.set_state(ReplyState.waiting_for_reply)  # Masuk ke state menunggu balasa
    except TelegramBadRequest:
        await callback.answer("⚠️ Waktu respon habis. Silakan klik tombol lagi.", show_alert=True)
    except Exception as e:
        logging.error(f"❌ Error saat menangani reply callback: {e}")
        await callback.answer("⚠️ Terjadi kesalahan saat mencoba membalas.", show_alert=True)

# Handler untuk menangkap balasan pengguna
@reply_to_sender_router.message(ReplyState.waiting_for_reply)
async def process_reply(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sender_id = data.get("sender_id")  # Ambil sender_id dari state

    if sender_id:
        try:
            await message.bot.send_message(sender_id, f"📩 Pesan dari pengirim:\n\n{message.text}", reply_markup=button_reply(message.from_user.id))
            await send_log_message(message, sender_id)
            await message.answer("✅ Pesan telah dikirim ke pengirim.")
        except Exception as e:
            logging.error(f"❌ Gagal mengirim pesan ke pengirim: {e}")
            await message.answer("⚠️ Tidak dapat mengirim pesan, mungkin pengguna telah memblokir bot.")
    else:
        await message.answer("⚠️ Terjadi kesalahan, sender tidak ditemukan.")

    await state.clear()  # Reset state setelah mengirim balasan
