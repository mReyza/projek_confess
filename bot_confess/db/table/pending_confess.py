from ..helpers import execute

async def init_db():
    await execute("""
        CREATE TABLE IF NOT EXISTS pending_confess (
            receiver_id INTEGER,
            sender_id INTEGER,
            message TEXT
        )
    """)
