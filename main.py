# -*- coding: utf-8 -*-

from bot import bot
from threading import Timer
from timer import check_time
import config
import logging
import handlers

if __name__ == "__main__":
    logger = logging.getLogger('bot')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger.setLevel(logging.DEBUG)
    if config.MODE == config.OFFLINE:
        t = Timer(config.CHECKER_TIME, check_time)
        t.start()
    bot.infinity_polling()

