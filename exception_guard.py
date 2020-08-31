# -*- coding: utf-8 -*-


def exception_guard(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print('EXCEPTION_GUARD:', str(error), args, kwargs)
            return 'Error'
    return wrapper
