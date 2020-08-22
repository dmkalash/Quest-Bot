# -*- coding: utf-8 -*-

import view
import pandas as pd
from exception_guard import exception_guard
from models import Team, OnPoint, OffPoint, OnReaction, OffReaction, File
from msg import messages
from config import *
from config import database

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
    data = pd.read_csv(ON_POINT_PATH)
    for index, row in data.iterrows():
        view.point.add_on_point(data['point_id'],
                                data['name'],
                                data['task'],
                                data['score'],
                                data['attempts'],
                                data['right_answer'],
                                data['artifacts'])
        print(index, 'OK')
    return SUCCESS

@exception_guard
def fill_off_points():
    data = pd.read_csv(OFF_POINT_PATH)
    for index, row in data.iterrows():
        view.point.add_off_point(data['id'],
                                 data['section'],
                                 data['name'],
                                 data['start_code'],
                                 data['finish_code'],
                                 data['task'],
                                 data['score'],
                                 data['fast'],
                                 data['middle'],
                                 data['slow'])
        print(index, 'OK')
    return SUCCESS

@exception_guard
def fill_on_reactions():
    data = pd.read_csv(ON_REACTION_PATH)
    for index, row in data.iterrows():
        view.reaction.add_reaction(ONLINE,
                                    row['text'],
                                    row['point_num'],
                                    row['order_num'])
        print(index, 'OK')
    return SUCCESS

@exception_guard
def fill_off_reactions():
    data = pd.read_csv(OFF_REACTION_PATH)
    for index, row in data.iterrows():
        view.reaction.add_reaction(OFFLINE,
                                    row['text'],
                                    row['point_num'],
                                    row['order_num'])
        print(index, 'OK')
    return SUCCESS

@exception_guard
def fill_files():
    data = pd.read_csv(FILE_PATH)
    for index, row in data.iterrows():
        view.file.add_file(row['file_id'],
                           row['point_num'],
                           row['order_num'],
                           row['file_type'])
        print(index, 'OK')
    return SUCCESS

@exception_guard
def add_file_id_to_txt(file_id):
    fout = open(FILE_PATH, 'a')
    print(file_id, file=fout)
    fout.close()
    return SUCCESS
