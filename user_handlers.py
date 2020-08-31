# -*- coding: utf-8 -*-

import view
from bot import bot
from config import MODE, ONLINE, RIGHT_ANSWER, WRONG_ANSWER, LAST_WRONG_ANSWER, ATTEMPT_WAS_LAST, ERROR, \
    PHOTO_TYPE, DOCUMENT_TYPE, AUDIO_TYPE
from data.messages import MSG_HELLO, MSG_ONLINE_START, MSG_ONLINE_END, MSG_OFFLINE_START, MSG_OFFLINE_END, MSG_HELP_ON, \
    MSG_HELP_OFF, MSG_SOS, MSG_NOT_RUNNING, MSG_NOT_OFF_RUNNING, MSG_NEED_CODE, MSG_WRONG_CODE, MSG_WRONG_POINT, \
    MSG_NEED_CHECK_IN, MSG_ALREADY_CHECKED_IN, MSG_WRONG_SECTION, MSG_TEAM, MSG_START_SPEAK, MSG_STOP_SPEAK, \
    MSG_PLAIN_TEXT, get_msg
from exception_guard import exception_guard
from handler_settings import online_mode, not_finished, offline_mode


@bot.message_handler(commands=["hello"])
@exception_guard
@online_mode
@not_finished
def hello(message):
    bot.send_message(message.chat.id, get_msg(MSG_HELLO))


@bot.message_handler(commands=["enter"])
@exception_guard
@online_mode
@not_finished
def enter(message):
    if not view.team.is_running(message.chat.id):
        view.team.on_game_start(message.chat.id)
        bot.send_message(message.chat.id, get_msg(MSG_ONLINE_START))
        send_task(message.chat.id)
    else:
        bot.send_message(message.chat.id, get_msg(MSG_NOT_RUNNING))


@bot.message_handler(commands=["skip"])
@exception_guard
@online_mode
@not_finished
def skip(message):
    if not view.team.is_running(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_NOT_RUNNING))
    else:
        view.team.next_online_level(message.chat.id, True)
        if view.team.is_finished(message.chat.id):
            bot.send_message(message.chat.id, get_msg(MSG_ONLINE_END))
        else:
            send_task(message.chat.id)


@bot.message_handler(commands=["kill"])
@exception_guard
@offline_mode
@not_finished
def kill(message):
    bot.send_message(message.chat.id, get_msg(MSG_OFFLINE_START))
    view.team.off_game_start(message.chat.id)


@bot.message_handler(commands=["help", "start"])
@exception_guard
def help(message):
    if MODE == ONLINE:
        bot.send_message(message.chat.id, get_msg(MSG_HELP_ON))
    else:
        bot.send_message(message.chat.id, get_msg(MSG_HELP_OFF))


@bot.message_handler(commands=["try"])
@exception_guard
@online_mode
@not_finished
def try_handler(message):
    if view.team.is_running(message.chat.id):
        text = message.text.split()[1]
        point = view.point.cur_point(message.chat.id)
        if point.right_answer.upper() == text.upper():
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
                if view.team.is_finished(message.chat.id):
                    bot.send_message(message.chat.id, get_msg(MSG_ONLINE_END))
                else:
                    send_task(message.chat.id)
            else:
                send_task(message.chat.id)
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
    if team == ERROR:
        bot.send_message(message.chat.id, ERROR)
    else:
        msg = get_msg(MSG_TEAM).format(team.name,
                                        team.participants,
                                        team.on_score + team.off_score,
                                        team.status,
                                        team.section)
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["task"])
@exception_guard
@online_mode
@not_finished
def task(message):
    if not view.team.is_running(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_NOT_RUNNING))
    else:
        send_task(message.chat.id)


@bot.message_handler(commands=["in"])
@exception_guard
@offline_mode
@not_finished
def check_in(message):
    if not view.team.is_running(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_NOT_OFF_RUNNING))
    elif view.team.is_team_responding(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_ALREADY_CHECKED_IN))
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


@bot.message_handler(commands=["out"])
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
            point = view.point.cur_point(message.chat.id)
            right_code = point.finish_code
            if code == right_code:
                reaction = view.reaction.get_answer_reaction(message.chat.id, RIGHT_ANSWER)
                bot.send_message(message.chat.id, reaction.text)
                view.team.next_offline_level(message.chat.id)
                if view.team.is_finished(message.chat.id):
                    bot.send_message(message.chat.id, get_msg(MSG_OFFLINE_END))
            else:
                bot.send_message(message.chat.id, get_msg(MSG_WRONG_CODE))


@bot.message_handler(commands=["speak"])
@exception_guard
def speak(message):
    view.team.change_bot_reaction(message.chat.id, True)
    bot.send_message(message.chat.id, get_msg(MSG_START_SPEAK))


@bot.message_handler(commands=["shut"])
@exception_guard
def shut(message):
    view.team.change_bot_reaction(message.chat.id, False)
    bot.send_message(message.chat.id, get_msg(MSG_STOP_SPEAK))


@bot.message_handler(content_types=["text"])
@exception_guard
def plain_text(message):
    if MODE == ONLINE:
        online_plain_text(message)
    else:
        offline_plain_text(message)


@exception_guard
def online_plain_text(message):
    if view.team.is_bot_speaking(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_PLAIN_TEXT))


@exception_guard
def offline_plain_text(message):
    if view.team.is_bot_speaking(message.chat.id):
        bot.send_message(message.chat.id, get_msg(MSG_PLAIN_TEXT))


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
            print('send_task problem: ', point, file.file_id, file.file_type)
