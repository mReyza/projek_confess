from ..helpers import execute, fetch_one

async def init_db():
    await execute("""
        CREATE TABLE IF NOT EXISTS relawan (
            relawan_id BIGINT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)