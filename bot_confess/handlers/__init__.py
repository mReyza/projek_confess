from .admin import admin_router
from .broadcast import router as broadcast_router
from .cekcoin_handler import cekcoin_router
from .coin_admin_handler import admin1_router
from .confess_handler import cancel_router, confess_router
from .feedback_handler import feedback_router
from .help_handler import help_router
from .reply_to_reciever_handler import reply_to_reciever_router
from .reply_to_sender_handler import reply_to_sender_router
from .start_handler import start_router
from .support_handler import support_router

all_routers = [
    reply_to_sender_router,
    reply_to_reciever_router,
    start_router,
    help_router,
    support_router,
    cancel_router,
    confess_router,
    feedback_router,
    admin_router,
    broadcast_router,
    cekcoin_router,
    admin1_router
]