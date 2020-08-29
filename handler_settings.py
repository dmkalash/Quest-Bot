# -*- coding: utf-8 -*-

import view
from bot import bot
from config import MODE, ONLINE, MSG_ONLINE_MODE, OFFLINE, MSG_OFFLINE_MODE, MSG_FINISHED, MSG_SUDO
from utils import get_msg, check_access


def online_mode(func):
    def wrapper(message):
        if MODE == ONLINE:
            func(message)
        else:
            bot.send_message(message.chat.id, get_msg(MSG_ONLINE_MODE))
    return wrapper


def offline_mode(func):
    def wrapper(message):
        if MODE == OFFLINE:
            func(message)
        else:
            bot.send_message(message.chat.id, get_msg(MSG_OFFLINE_MODE))
    return wrapper


def not_finished(func):
    def wrapper(message):
        if not view.team.is_finished(message.chat.id):
            func(message)
        else:
            bot.send_message(message.chat.id, get_msg(MSG_FINISHED))
    return wrapper


def sudo(func):
    def wrapper(message):
        if check_access(message.from_user.id):
            func(message)
        else:
            bot.send_message(message.chat.id, get_msg(MSG_SUDO))
    return wrapper