from typing import Union
from aiogram.types import Message, CallbackQuery
from config.config_admin import ADMIN_IDS

from .broadcast import router as r1
from .coin_admin_handler import router as r2
from .stats import router as r3

admin_router = [
    r1,
    r2,
    r3
]

# Custom filter tanpa BaseFilter
async def admin_filter(event: Union[Message | CallbackQuery]) -> bool:
    return event.from_user.id in ADMIN_IDS

for router in admin_router:
    router.message.filter(admin_filter)
    router.callback_query.filter(admin_filter)
