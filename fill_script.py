# -*- coding: utf-8 -*-
from utils import create_tables, fill_on_points, fill_off_points, fill_on_reactions, fill_off_reactions, fill_files
from config import NEED_TO_FILL_DB

def fill_script():
    if not NEED_TO_FILL_DB:
        print('Not needed to fill database')
    else:
        print('create_tables', create_tables())
        print('on_points:', fill_on_points())
        print('off_points:', fill_off_points())
        print('on_reactions:', fill_on_reactions())
        print('off_reactions:', fill_off_reactions())
        print('fill_files:', fill_files())
