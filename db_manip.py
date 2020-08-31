from db_init import database
from exception_guard import exception_guard
from models import Team, OnPoint, OffPoint, OnReaction, OffReaction, File
from msg.messages import get_msg, MSG_SUCCESS


@exception_guard
def create_tables():
    with database:
        database.create_tables([Team, OnPoint, OffPoint, OnReaction, OffReaction, File])
        return get_msg(MSG_SUCCESS)


@exception_guard
def drop_tables():
    with database:
        database.drop_tables([Team, OnPoint, OffPoint, OnReaction, OffReaction, File])
        return get_msg(MSG_SUCCESS)
