# -*- coding: utf-8 -*-

import view
from bot import bot
from config import SUCCESS, MSG_PINNED, ERROR
from exception_guard import exception_guard
from fill_script import fill_script
from handler_settings import sudo, online_mode, offline_mode
from utils import get_msg, drop_tables


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
        bot.send_message(message.chat.id, "/reg TeamName PartCount Section")
    else:
        if view.team.add_team(message.chat.id, name, int(part_count), int(section)) != ERROR:
            bot.send_message(message.chat.id, 'OK')
        else:
            bot.send_message(message.chat.id, 'ERROR')


@bot.message_handler(commands=["set_section"])
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
