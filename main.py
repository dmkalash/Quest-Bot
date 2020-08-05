# -*- coding: utf-8 -*-

from bot import bot
from threading import Timer
import config
import logging
import handlers

if __name__ == "__main__":
    logger = logging.getLogger('vmquest')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.setLevel(logging.DEBUG)
    config.database = config.db_init()
    config.database.connect()

    from timer import check_time
    if config.MODE == config.OFFLINE:
        t = Timer(config.CHECKER_TIME, check_time)
        t.start()
    bot.infinity_polling()
