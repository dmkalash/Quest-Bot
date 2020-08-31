# -*- coding: utf-8 -*-

from db_init import database
from bot import bot
from threading import Timer
from config import MODE, OFFLINE, CHECKER_TIME
import logging
import util_handlers
import user_handlers


# TODO: решить, делать ли тесты
# TODO: гайд перееписать

if __name__ == "__main__":
    logger = logging.getLogger('vmquest')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.setLevel(logging.DEBUG)

    database.connect()

    from timer import check_time
    if MODE == OFFLINE:
        t = Timer(CHECKER_TIME, check_time)
        t.start()
    bot.infinity_polling()
