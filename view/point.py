# -*- coding: utf-8 -*-

import view
from config import *
from models import OnPoint, OffPoint
from exception_guard import exception_guard

@exception_guard
def add_on_point(**kwargs):
    point = OnPoint.create(**kwargs)
    return point

@exception_guard
def add_off_point(**kwargs):
    point = OffPoint.create(**kwargs)
    return point

@exception_guard
def get_point(id, section = 0):
    if MODE == ONLINE:
        point = OnPoint.get(OnPoint.id == id)
    else:
        point = OffPoint.get(OffPoint.id == id, OffPoint.section == section)
    return point

@exception_guard
def cur_point(chat_id):
    team = view.team.get_team(chat_id)
    if MODE == ONLINE:
        point_id = team.on_point
    else:
        point_id = team.off_point
    return get_point(point_id, team.section)

@exception_guard
def get_off_point_with_code(code):
    return OffPoint.get(OffPoint.start_code == code)

###

@exception_guard
def delete_point(id, section):
    point = get_point(id, section)
    point.delete_instance()
