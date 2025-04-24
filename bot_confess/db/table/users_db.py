from ..helpers import execute, fetch_one

async def init_db():
    await execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            coin BIGINT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

async def get_coin_user(user_id: int):
     user = await fetch_one("SELECT coin FROM users WHERE user_id = $1", user_id)
     return user[0]
    
async def manager_coin(user_id: int, coin_amount: int):
    await execute("UPDATE users SET coin = coin + $1 WHERE user_id = $2", coin_amount, user_id)