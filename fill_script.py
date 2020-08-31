# -*- coding: utf-8 -*-
from db_utils.db_manip import create_tables
from fill import FillFactory
from config import *


def fill_script():
    print(create_tables())
    factory = FillFactory()
    factory.fill(ON_POINT_KEY, 'data/' + ON_POINT_KEY + '.csv')
    factory.fill(OFF_POINT_KEY, 'data/' + OFF_POINT_KEY + '.csv')
    factory.fill(REACTION_KEY, 'data/' + REACTION_KEY + '.csv')
    factory.fill(FILE_KEY, 'data/' + FILE_KEY + '.csv')
