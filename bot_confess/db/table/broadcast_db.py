from ..helpers import execute

async def init_db():
    await execute("""
        CREATE TABLE IF NOT EXISTS broadcast_messages (
            id BIGSERIAL PRIMARY KEY,
            message_id BIGINT NOT NULL,
            chat_id BIGINT NOT NULL
        )
    """)
