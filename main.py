# -*- coding: utf-8 -*-

from db_init import database
from bot import bot
from threading import Timer
import config
import logging
import util_handlers
import user_handlers


# TODO: сделать листинг команд для разраба отдельной командой
# TODO: решить, делать ли тесты
# TODO: нормальные отступы
# TODO: сделать /next для "пояснительных" КП. Их признак - score == 0. Ничего не выводить, просто след уровень и таск
# TODO: сделать другой критерий окончания квеста, а не числа их конфига
# TODO: гайд перееписать

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
