# -*- coding: utf-8 -*-

from bot import bot
from threading import Timer
from timer import check_time
import config
import handlers
import fill_script

if __name__ == '__main__':
    config.database.connect()
    if config.MODE == config.OFFLINE:
        t = Timer(config.CHECKER_TIME, check_time)
        t.start()
    bot.infinity_polling()
