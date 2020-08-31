# -*- coding: utf-8 -*-
# CREATED by Dmitry Kalashnikov, 2020.
# https://github.com/dmkalash
# https://vk.com/dmkalash


from db_utils.db_init import database
from bot import bot
from threading import Timer
from config import MODE, OFFLINE, CHECKER_TIME
import logging
from handlers import util_handlers, user_handlers


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
