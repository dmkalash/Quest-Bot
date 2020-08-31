# -*- coding: utf-8 -*-

import view
from bot import bot
from config import SUCCESS, ERROR
from data.messages import MSG_PINNED, MSG_REG_INFO, MSG_SUCCESS, MSG_ERROR, MSG_UTIL, get_msg
from exception_guard import exception_guard
from db_utils.fill_script import fill_script
from handler_settings import sudo, online_mode, offline_mode
from db_utils.db_manip import drop_tables


@bot.message_handler(commands=["util"])
@exception_guard
@sudo
def util(message):
    bot.send_message(message.chat.id, get_msg(MSG_UTIL))


@bot.message_handler(commands=["fill"])
@exception_guard
@sudo
def fill(message):
    fill_script()
    bot.send_message(message.chat.id, SUCCESS)


@bot.message_handler(commands=["pinned"])
@exception_guard
@sudo
@online_mode
def pinned(message):
    bot.send_message(message.chat.id, get_msg(MSG_PINNED))


@bot.message_handler(commands=["flush"])
@exception_guard
@sudo
@offline_mode
def status_flush(message):
    bot.send_message(message.chat.id, view.team.flush_team_status())


@bot.message_handler(commands=["reg"])
@exception_guard
@online_mode
@sudo
def reg(message):
    try:
        name, part_count, section = message.text.split()[1:]
    except:
        bot.send_message(message.chat.id, get_msg(MSG_REG_INFO))
    else:
        if view.team.add_team(message.chat.id, name, int(part_count), int(section)) != ERROR:
            bot.send_message(message.chat.id, get_msg(MSG_SUCCESS))
        else:
            bot.send_message(message.chat.id, get_msg(MSG_ERROR))


@bot.message_handler(commands=["section"])
@exception_guard
@sudo
@online_mode
def set_section(message):
    section = int(message.text.split()[1])
    bot.send_message(message.chat.id, view.team.set_section(message.chat.id, section))


@bot.message_handler(commands=["unreg"])
@exception_guard
@sudo
def unreg(message):
    bot.send_message(message.chat.id, view.team.delete_team(message.chat.id))


@bot.message_handler(commands=["reset"])
@exception_guard
@sudo
def reset(message):
    bot.send_message(message.chat.id, drop_tables())


@bot.message_handler(content_types=["photo", "document", "audio"])
@exception_guard
@sudo
def send_files(message):
    if message.content_type == 'photo':
        file_id = message.photo[0].file_id
    elif message.content_type == 'document':
        file_id = message.document.file_id
    else:
        file_id = message.audio.file_id
    file_id = file_id + '\n'
    bot.send_message(message.chat.id, file_id)
