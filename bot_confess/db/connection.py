# db/connection.py

import asyncpg
import logging
import traceback
from contextlib import asynccontextmanager
from config.config_db import DATABASE_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Logging ke file
file_handler = logging.FileHandler("db_errors.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Pool koneksi global
pool = None

async def init_db():
    """Inisialisasi koneksi database dengan pool."""
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)
    print("Database pool initialized!")

async def close_db():
    """Menutup koneksi pool database saat aplikasi ditutup."""
    global pool
    if pool:
        await pool.close()
        print("Database pool closed!")

@asynccontextmanager
async def get_connection():
    """Context manager untuk ambil 1 koneksi dari pool."""
    global pool
    if not pool:
        raise RuntimeError("Pool belum diinisialisasi. Panggil init_db() terlebih dahulu.")
    conn = await pool.acquire()
    try:
        yield conn
    except Exception as e:
        logger.error(f"[DB ERROR] {e}\n{traceback.format_exc()}")
        raise
    finally:
        await pool.release(conn)
