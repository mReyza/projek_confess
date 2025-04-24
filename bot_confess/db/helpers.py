# db/helpers.py

import traceback
import logging
from contextlib import asynccontextmanager
from .connection import get_connection

logger = logging.getLogger(__name__)

@asynccontextmanager
async def transactional_connection():
    """
    Context manager untuk koneksi dengan transaksi.
    Otomatis COMMIT jika berhasil, atau ROLLBACK jika error.
    """
    async with get_connection() as conn:
        tx = conn.transaction()
        await tx.start()
        try:
            yield conn
            await tx.commit()
        except Exception as e:
            await tx.rollback()
            logger.error(f"[TRANSACTION ERROR] {e}\n{traceback.format_exc()}")
            raise

async def execute(query: str, *args):
    """Menjalankan query yang tidak mengembalikan hasil (INSERT/UPDATE/DELETE)."""
    async with get_connection() as conn:
        return await conn.execute(query, *args)

async def fetch_one(query: str, *args):
    """Mengambil satu baris hasil dari query."""
    async with get_connection() as conn:
        return await conn.fetchrow(query, *args)

async def fetch_all(query: str, *args):
    """Mengambil semua baris hasil dari query."""
    async with get_connection() as conn:
        return await conn.fetch(query, *args)
