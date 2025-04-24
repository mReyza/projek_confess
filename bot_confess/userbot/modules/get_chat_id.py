import requests
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 28913594
API_HASH = "fb5991cce4545b6b3a0c4ad5132df2a9"
SESSION_STRING = "1BVtsOJ8Bu4Kt-jU6s0iQb5TdDyAmKEcE8NlzaA4XAlv0pprW8zKaLRDvV0IStSRaWP12xgCkIZrt-PKXKYvvq-FtKAz4ZRU2DXeccSirK9IL6hKdBUmix6Ca_RPslPTp6j7qqg1EmXRMNjw3jAoiYBtQ6GmN7sbSN-5ql9hRZj_g2Mv52cC0Qy19vBEsUfA9ksAO_xW_6--WYskDcFBDAjaIu_PGMGjabJI_RNac4pl_VnFVEC191V2FkEGXcpTOtAjFu6KVEK29caO9tWdALi7_WDJmyz8IHsQl0S-Z9tWwlK_RphwujlZ2PMrptDqDr1A28uKtXRYR-RaBI1frR7i_SNLzgTE="

session = StringSession(SESSION_STRING)
client = TelegramClient(session, API_ID, API_HASH)

async def get_user_id_telethon(username):
    """ Mendapatkan ID pengguna menggunakan Telethon """
    try:
        async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
            user = await client.get_entity(username)
            return user.id
    except Exception as e:
        print(f"Telethon Error: {e}")
        return None
    
async def send_message(message, username):
    """ Mengirim pesan ke pengguna Telegram """
    try:
        async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
            await client.send_message(username, message)
            print(f"Pesan berhasil dikirim ke {username}")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
