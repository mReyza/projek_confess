from .pending_confess import init_db as db2
from .users_db import init_db as db1


def init_db():
    db1(),
    db2()