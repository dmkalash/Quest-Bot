from config import ERROR

def exception_guard(func): # TODO: выводить в лс с админами из config эти исключения
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print('EXCEPTION_GUARD:', str(error), args, kwargs)
            return ERROR
    return wrapper
