# -*- coding: utf-8 -*-

from datetime import datetime
from threading import Timer

import view
from config import *
from data.messages import MSG_OFFLINE_END, get_msg
from bot import bot


def check_time():
    for team in view.team.get_all_teams():
        if not team.responding:
            continue
        start_time = team.cur_start_time
        cur_point = view.point.get_point(team.off_point, team.section)
        time_delta = (datetime.now() - start_time).total_seconds() // 60
        attempt_num = team.attempt_num
        if attempt_num == MIDDLE_ATTEMPT and time_delta >= cur_point.slow:
            reaction = view.reaction.get_answer_reaction(team.chat_id, LAST_WRONG_ANSWER)
            bot.send_message(team.chat_id, reaction.text)
            view.team.set_wrong(team.chat_id)
            if view.team.is_finished(team.chat_id):
                bot.send_message(team.chat_id, get_msg(MSG_OFFLINE_END))
        elif attempt_num == FAST_ATTEMPT and time_delta >= cur_point.middle:
            view.team.set_wrong(team.chat_id)
            reaction = view.reaction.get_answer_reaction(team.chat_id, WRONG_ANSWER)
            bot.send_message(team.chat_id, reaction.text)
        elif attempt_num == RUN_ATTEMPT and time_delta >= cur_point.fast:
            view.team.set_wrong(team.chat_id)
            reaction = view.reaction.get_answer_reaction(team.chat_id, WRONG_ANSWER)
            bot.send_message(team.chat_id, reaction.text)
    t = Timer(CHECKER_TIME, check_time)
    t.start()
