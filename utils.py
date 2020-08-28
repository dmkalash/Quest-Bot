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
def add_file_id_to_txt(file_id):
    fout = open(FILE_ID_PATH, 'a')
    print(file_id, file=fout)
    fout.close()
    return SUCCESS
