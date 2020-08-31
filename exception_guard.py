from utils import get_msg
from msg.messages import MSG_ERROR


def exception_guard(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print('EXCEPTION_GUARD:', str(error), args, kwargs)
            return get_msg(MSG_ERROR)
    return wrapper
