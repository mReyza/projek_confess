from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import logging


@router.callback_query(F.data == "via_bot")
async def process_confess_option(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_text = data.get("msg_text")
    receiver_id = data.get("receiver_id")
    sender_id = data.get("sender_id")
    username = data.get("username")

    try:
        await callback.bot.send_message(
            chat_id=receiver_id,
            text=f"💌 Wahh.. Ada yang confess ke kamu nih!\n\nPesan: {msg_text}",
            reply_markup=button_reply(sender_id)
        )
        await send_log_message(callback, receiver_id)
        await callback.message.edit_text("✅ Confess kamu berhasil dikirim!")

    except Exception as e:
        logging.error(f"❌ Gagal mengirim pesan ke @{username}: {e}")
        save_failed_message(receiver_id, sender_id, msg_text)  # Fungsi untuk simpan ke DB
        try:
            await send_message(
                f"Seseorang mengirimmu confess! \n\n{msg_text}\n\n"
                f"Ingin membalas confess ini? Tekan dan balas di @anonymous_confess_bot!",
                username
            )
        except Exception as notify_err:
            logging.warning(f"Gagal kirim notifikasi ke @{username}: {notify_err}")
        await callback.message.edit_text("⚠️ Pesanmu tersimpan! Pastikan username yang kamu tuju sudah pernah chat bot.")

    await state.clear()
