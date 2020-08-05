# -*- coding: utf-8 -*-

import view
from exception_guard import exception_guard
from models import Team, OnPoint, OffPoint, OnReaction, OffReaction, File
from msg import messages
from config import *
from config import database

@exception_guard
def read_data_line(fin):
    line = fin.readline()[:-1]
    if len(line) != 0 and line[0] == '<':
        while line[-1] != '>':
            line = line + '\n' + fin.readline()[:-1]
        return line[1:-1]
    else:
        return line

@exception_guard
def get_msg(alias):
    return messages.messages.get(alias)

@exception_guard
def create_tables():
    with database:
        database.create_tables([Team, OnPoint, OffPoint, OnReaction, OffReaction, File])
        return SUCCESS

@exception_guard
def check_access(user_id):
    return user_id in ADMIN_USER_IDS

@exception_guard
def fill_on_points():
    fin = open(ON_POINT_PATH, 'r')
    num = 1
    while True:
        point_id = int(read_data_line(fin))
        name = read_data_line(fin)
        task = read_data_line(fin)
        score = int(read_data_line(fin))
        attempts = int(read_data_line(fin))
        right_answer = read_data_line(fin)
        artifacts = int(read_data_line(fin))
        view.point.add_on_point(point_id, name, task, score, attempts, right_answer, artifacts)
        print(num, 'OK')
        num += 1
        if read_data_line(fin) == EOF_MARKER:
            break
    fin.close()
    return SUCCESS

@exception_guard
def fill_off_points():
    fin = open(OFF_POINT_PATH, 'r')
    num = 1
    while True:
        id = int(read_data_line(fin))
        name = read_data_line(fin)
        start_code = read_data_line(fin)
        finish_code = read_data_line(fin)
        task = read_data_line(fin)
        score = int(read_data_line(fin))
        fast = int(read_data_line(fin))
        middle = int(read_data_line(fin))
        slow = int(read_data_line(fin))
        view.point.add_off_point(id, name, start_code, finish_code, task, score, fast, middle, slow)
        print(num, 'OK')
        num += 1
        if read_data_line(fin) == EOF_MARKER:
            break
    fin.close()
    return SUCCESS

@exception_guard
def fill_on_reactions():
    fin = open(ON_REACTION_PATH, 'r')
    num = 1
    while True:
        text = read_data_line(fin)
        point_num = int(read_data_line(fin))
        order_num = int(read_data_line(fin))
        view.reaction.add_reaction(ONLINE, text, point_num, order_num)
        print(num, 'OK')
        num += 1
        if read_data_line(fin) == EOF_MARKER:
            break
    fin.close()
    return SUCCESS

@exception_guard
def fill_off_reactions():
    fin = open(OFF_REACTION_PATH, 'r')
    num = 1
    while True:
        text = read_data_line(fin)
        point_num = int(read_data_line(fin))
        order_num = int(read_data_line(fin))
        view.reaction.add_reaction(OFFLINE, text, point_num, order_num)
        print(num, 'OK')
        num += 1
        if read_data_line(fin) == EOF_MARKER:
            break
    fin.close()
    return SUCCESS

@exception_guard
def fill_files():
    fin = open(FILE_PATH, 'r')
    num = 1
    while True:
        file_id = read_data_line(fin)
        point_num = int(read_data_line(fin))
        order_num = int(read_data_line(fin))
        file_type = int(read_data_line(fin))
        cur_point = view.point.get_point(point_num)
        view.file.add_file(file_id, order_num, cur_point, file_type)
        print(num, 'OK')
        num += 1
        if read_data_line(fin) == EOF_MARKER:
            break
    fin.close()
    return SUCCESS

@exception_guard
def add_file_id_to_txt(file_id):
    fout = open(FILE_PATH, 'a')
    print(file_id, file=fout)
    fout.close()
    return SUCCESS
