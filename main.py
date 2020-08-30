# -*- coding: utf-8 -*-

from db_init import database
from bot import bot
from threading import Timer
#import db_init
import config
import logging
import util_handlers
import user_handlers

# TODO: db_init в отдельный файл
# TODO: сделать все команды удобнее
# TODO: сделать листинг команд для разраба отдельной командой
# TODO: выделить все константные ответы в messages
# TODO: решить, делать ли тесты

if __name__ == "__main__":
    logger = logging.getLogger('vmquest')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.setLevel(logging.DEBUG)

    database.connect()

    from timer import check_time
    if config.MODE == config.OFFLINE:
        t = Timer(config.CHECKER_TIME, check_time)
        t.start()
    bot.infinity_polling()
