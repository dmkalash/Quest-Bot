# -*- coding: utf-8 -*-

import view
from bot import bot
from config import MODE, ONLINE, OFFLINE, ADMIN_USER_IDS
from data.messages import MSG_ONLINE_MODE, MSG_OFFLINE_MODE, MSG_FINISHED, MSG_SUDO, get_msg


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
        if message.from_user.id in ADMIN_USER_IDS:
            func(message)
        else:
            bot.send_message(message.chat.id, get_msg(MSG_SUDO))
    return wrapper