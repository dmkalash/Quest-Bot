from config import ERROR

def exception_guard(func): # TODO: выводить в лс с админами из config эти исключения
    def wrapper(*args):
        try:
            return func(*args)
        except Exception as error:
            print('EXCEPTION_GUARD:', str(error), args)
            return ERROR
    return wrapper