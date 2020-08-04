# -*- coding: utf-8 -*-

from bot import bot
from config import *
from threading import Timer
from timer import check_time
import handlers

if __name__ == '__main__':
    if MODE == OFFLINE:
        t = Timer(CHECKER_TIME, check_time)
        t.start()
    bot.infinity_polling()
