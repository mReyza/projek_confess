from aiogram import Router, types, Bot
from aiogram.filters import Command
import asyncio
import logging
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter, TelegramBadRequest
from db.connection import get_connection

router = Router()

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BROADCAST_RATE = 10  # Jumlah pesan per detik

# Fungsi untuk mengirim pesan
async def send_message(bot: Bot, id: int, text: str):
    try:
        sent_message = await bot.send_message(id, text)
        log.info("Target [ID:%d]: success", id)
        return sent_message.message_id, False  # Kembali message_id dan status 'removed'
    except TelegramRetryAfter as e:
        log.error("Target [ID:%d]: Flood limit exceeded. Sleep %d seconds.", id, e.retry_after)
        await asyncio.sleep(e.retry_after)
        return await send_message(bot, id, text)  # Recursive call
    except TelegramAPIError as e:
        error_message = str(e)
        removed = False
        if "bot was blocked by the user" in error_message:
            log.error("Target [ID:%d]: blocked by user", id)
            await remove_user_from_db(id)
            removed = True
        elif "chat not found" in error_message:
            log.error("Target [ID:%d]: invalid user ID", id)
            await remove_user_from_db(id)
            removed = True
        elif "user is deactivated" in error_message:
            log.error("Target [ID:%d]: user is deactivated", id)
            await remove_user_from_db(id)
            removed = True
        else:
            log.exception("Target [ID:%d]: failed with error: %s", id, e)

        return None, removed  # Kembali None dan status 'removed'

# Fungsi untuk menghapus pengguna dari database
async def remove_user_from_db(id: int):
    async with get_connection() as conn:
        await conn.execute('DELETE FROM users WHERE user_id = $1', id)
        log.info("User [ID:%d] removed from database", id)

# Fungsi untuk menambahkan entri ke dalam tabel log broadcast
async def add_broadcast_entry(message_id: int, chat_id: int):
    async with get_connection() as conn:
        await conn.execute(
            'INSERT INTO broadcast_messages (message_id, chat_id) VALUES ($1, $2)',
            message_id, chat_id
        )

# Fungsi utama untuk broadcast pesan
async def broadcast(bot: Bot, text: str):
    async with get_connection() as conn:
        users = await conn.fetch('SELECT user_id FROM users')

    total_users = len(users)
    success_count = 0
    failed_count = 0
    removed_count = 0
    processed_count = 0

    for user in users:
        if processed_count % BROADCAST_RATE == 0 and processed_count > 0:
            await asyncio.sleep(1)  # Pause setiap BROADCAST_RATE pesan

        id = user['user_id']
        message_id, is_removed = await send_message(bot, id, text)

        if message_id:  # Jika pengiriman berhasil
            success_count += 1
            await add_broadcast_entry(message_id, id)  # Simpan entri log
        else:
            failed_count += 1

        if is_removed:
            removed_count += 1

        processed_count += 1
        log.info("Broadcast progress: %d/%d (Success: %d, Failed: %d, Removed: %d)",
                 processed_count, total_users, success_count, failed_count, removed_count)

    log.info("Broadcast completed. Success: %d, Failed: %d, Removed: %d",
             success_count, failed_count, removed_count)

    return total_users, success_count, failed_count, removed_count

@router.message(Command("deletebroadcastmessage"))
async def cmd_delete_broadcast_message(message: types.Message, bot: Bot):
    async with get_connection() as conn:
        broadcast_messages = await conn.fetch('SELECT message_id, chat_id FROM broadcast_messages')

    total_messages = len(broadcast_messages)
    if total_messages == 0:
        await message.reply("Tidak ada pesan untuk dihapus.")
        return

    status_message = await message.answer("Menghapus pesan broadcast. Mohon tunggu hingga selesai...")
    deleted_count = 0
    failed_count = 0

    for record in broadcast_messages:
        message_id, chat_id = record['message_id'], record['chat_id']
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            await remove_broadcast_entry(message_id)
            deleted_count += 1
            log.info(f"Deleted broadcast message [ID:{message_id}] from chat [ID:{chat_id}]")
        except TelegramBadRequest as e:
            if "message identifier is not specified" in str(e) or "chat not found" in str(e):
                await remove_broadcast_entry(message_id)
                failed_count += 1
                log.warning(f"Could not delete message [ID:{message_id}] from chat [ID:{chat_id}]: {e}")
            else:
                raise
        except Exception as e:
            failed_count += 1
            log.error(f"Error processing message [ID:{message_id}]: {e}")

        if (deleted_count + failed_count) % 10 == 0:
            await asyncio.sleep(1)  # Pause setiap 10 pesan

    report_message = (
        f"<b>Laporan Penghapusan Pesan Broadcast Selesai</b>\n\n"
        f"Total Pesan Dihapus: {deleted_count}\n"
        f"Pesan yang gagal dihapus: {failed_count}"
    )

    await status_message.edit_text(report_message, parse_mode="HTML")

# Fungsi untuk menghapus entri broadcast dari database
async def remove_broadcast_entry(message_id: int):
    async with get_connection() as conn:
        await conn.execute('DELETE FROM broadcast_messages WHERE message_id = $1', message_id)
        log.info(f"Broadcast message [ID:{message_id}] removed from database")

@router.message(Command("broadcastdb"))
async def cmd_broadcast_db(message: types.Message, bot: Bot):
    if not message.reply_to_message or not message.reply_to_message.text:
        await message.reply("Gunakan perintah ini dengan mereply pesan yang ingin dibroadcast.")
        return

    broadcast_content = message.reply_to_message.text
    status_message = await message.answer("Broadcast dimulai. Mohon tunggu hingga selesai...")
    total_users, success_count, failed_count, removed_count = await broadcast(bot, broadcast_content)

    report_message = (
        f"<b>Laporan Broadcast Selesai</b>\n\n"
        f"Total Pengguna: {total_users}\n"
        f"Pesan Terkirim: {success_count}\n"
        f"Pesan Gagal: {failed_count}\n"
        f"Pengguna Dihapus: {removed_count}"
    )

    await status_message.edit_text(report_message, parse_mode="HTML")
