# -*- coding: utf-8 -*-

import view
from utils import check_access, get_msg, add_file_id_to_txt
from exception_guard import exception_guard
from fill_script import fill_script
from bot import bot
from config import *

##### Decorators
# TODO: сделать команду выключения ответок бота
# TODO: сделать команду удаления базы данных
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

##### Handlers

@bot.message_handler(commands=["fill"])
@exception_guard
@sudo
def fill(message):
    fill_script()
    bot.send_message(message.chat.id, SUCCESS)

@bot.message_handler(commands=["hello"])
@exception_guard
@online_mode
@not_finished
def hello(message):
    bot.send_message(message.chat.id, get_msg(MSG_HELLO))

@bot.message_handler(commands=["pinned"])
@exception_guard
@sudo
@online_mode
def pinned(message):
    bot.send_message(message.chat.id, get_msg(MSG_PINNED))

@bot.message_handler(commands=["enter"])
@exception_guard
@online_mode
@not_finished
def enter(message):
    view.team.on_game_start(message.chat.id)
    bot.send_message(message.chat.id, get_msg(MSG_ONLINE_START))
    send_task(message.chat.id)

@bot.message_handler(commands=["kill"])
@exception_guard
@offline_mode
@not_finished
def kill(message):
    bot.send_message(message.chat.id, get_msg(MSG_OFFLINE_START))
    view.team.off_game_start(message.chat.id)

@bot.message_handler(commands=["flush"])
@exception_guard
@sudo
@offline_mode
def status_flush(message):
    bot.send_message(message.chat.id, view.team.flush_team_status())

@bot.message_handler(commands=["help", "start"])
@exception_guard
def help(message):
    if MODE == ONLINE:
        bot.send_message(message.chat.id, get_msg(MSG_HELP_ON))
    else:
        bot.send_message(message.chat.id, get_msg(MSG_HELP_OFF))

@bot.message_handler(commands=["answer"])
@exception_guard
@online_mode
@not_finished
def answer(message):
    if view.team.is_running(message.chat.id):
        view.team.set_team_responding(message.chat.id)
        bot.send_message(message.chat.id, get_msg(MSG_ANSWER))
    else:
        bot.send_message(message.chat.id, get_msg(MSG_NOT_RUNNING))

@bot.message_handler(commands=["sos"])
@exception_guard
def sos(message):
    bot.send_message(message.chat.id, get_msg(MSG_SOS))

@bot.message_handler(commands=["team"])
@exception_guard
def team(message):
    team = view.team.get_team(message.chat.id)
    print(team, team == ERROR, type(team), ERROR, type(ERROR))
    if team == ERROR:
        print('HERE!!!!')
        bot.message_handler(message.chat.id, ERROR)
    else:
        msg = "Название: {}\nКоличество участников: {}\nИнтеллект: {}\nСтатус: {}\nКруг: {}".format(
            team.name, team.participants, team.on_score + team.off_score, team.status, team.section)
        bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=["reg"])
@exception_guard
@sudo
def reg(message):
    name, part_count, section = message.text.split()[1:]
    if view.team.add_team(message.chat.id, name, int(part_count), int(section)) != ERROR:
        bot.send_message(message.chat.id, 'OK')

@bot.message_handler(commands=["set_section"])
@exception_guard
@sudo
@online_mode
def set_section(message):
    section = int(message.text.split()[1])
    bot.send_message(message.chat.id, view.team.set_section(message.chat.id, section))

@bot.message_handler(commands=["checkin"])
@exception_guard
@offline_mode
@not_finished
def check_in(message): # TODO: сделать у ОФФКП номер круга, у команды - номер круга, и у разных кругов разные коды
    if not view.team.is_running(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_NOT_OFF_RUNNING))
    elif view.team.is_team_responding(message.chat.id):
        bot.send_message(message.chat.id, get_msg(ALREADY_CHECKED_IN))
    else:
        try:
            code = message.text.split()[1]
        except IndexError:
            bot.send_message(message.chat.id, get_msg(MSG_NEED_CODE))
        else:
            point = view.point.get_off_point_with_code(code)
            if point == ERROR:
                bot.send_message(message.chat.id, get_msg(MSG_WRONG_CODE))
            elif point.id != view.point.cur_point(message.chat.id).id:
                bot.send_message(message.chat.id, get_msg(MSG_WRONG_POINT))
            elif point.section != view.team.get_section(message.chat.id):
                bot.send_message(message.chat.id, get_msg(MSG_WRONG_SECTION))
            else:
                bot.send_message(message.chat.id, point.task)
                view.team.set_team_responding(message.chat.id)
                view.team.set_cur_time(message.chat.id)

@bot.message_handler(commands=["checkout"])
@exception_guard
@offline_mode
@not_finished
def check_out(message):
    if not view.team.is_team_responding(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_NEED_CHECK_IN))
    else:
        try:
            code = message.text.split()[1]
        except IndexError:
            bot.send_message(get_msg(MSG_NEED_CODE))
        else:
            right_code = view.point.cur_point(message.chat.id).finish_code
            if code == right_code:
                reaction = view.reaction.get_answer_reaction(message.chat.id, RIGHT_ANSWER)
                bot.send_message(message.chat.id, reaction.text)
                view.team.next_offline_level(message.chat.id)
                if view.team.is_finished(message.chat.id):
                    bot.send_message(message.chat.id, get_msg(MSG_OFFLINE_END))
            else:
                bot.send_message(message.chat.id, get_msg(MSG_WRONG_CODE))

@bot.message_handler(commands=["delete_team"])
@exception_guard
@sudo
def delete_team(message):
    bot.send_message(message.chat.id, view.team.delete_team(message.chat.id))

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
    file_id = message.caption + '\n' + file_id + '\n'
    bot.send_message(message.chat.id, file_id)
    print('add_file_to_txt: ', add_file_id_to_txt(file_id))

@bot.message_handler(content_types=["text"])
@exception_guard
def plain_text(message):
    print(message.text)
    if MODE == ONLINE:
        online_plain_text(message)
    else:
        offline_plain_text(message)

@exception_guard
def online_plain_text(message):
    if view.team.is_team_responding(message.chat.id):
        point = view.point.cur_point(message.chat.id)
        if point.right_answer.upper() == message.text.upper():
            reaction = view.reaction.get_answer_reaction(message.chat.id, RIGHT_ANSWER)
            bot.send_message(message.chat.id, reaction.text)
            view.team.next_online_level(message.chat.id)
            if view.team.is_finished(message.chat.id):
                bot.send_message(message.chat.id, get_msg(MSG_ONLINE_END))
            else:
                send_task(message.chat.id)
        else:
            reaction = view.reaction.get_answer_reaction(message.chat.id, WRONG_ANSWER)
            bot.send_message(message.chat.id, reaction.text)
            last_reaction = view.reaction.get_answer_reaction(message.chat.id, LAST_WRONG_ANSWER)
            if view.team.set_wrong(message.chat.id) == ATTEMPT_WAS_LAST:
                bot.send_message(message.chat.id, last_reaction.text)
            send_task(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'И не говори')

@exception_guard
def offline_plain_text(message):
    bot.send_message(message.chat.id, 'И не говори')

@exception_guard
def send_task(chat_id):
    point = view.point.cur_point(chat_id)
    bot.send_message(chat_id, point.task)
    for file in view.file.get_files_with_point(point):
        if file.file_type == PHOTO_TYPE:
            bot.send_photo(chat_id, file.file_id)
        elif file.file_type == DOCUMENT_TYPE:
            bot.send_document(chat_id, file.file_id)
        elif file.file_type == AUDIO_TYPE:
            bot.send_audio(chat_id, file.file_id)
        else:
            print('send_task problem', point, file.file_id, file.file_type)

