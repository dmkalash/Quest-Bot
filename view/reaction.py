# -*- coding: utf-8 -*-

import view
from config import *
from models import OnReaction, OffReaction
from exception_guard import exception_guard

@exception_guard
def add_reaction(point_type, text, point_num, order_num):
    if point_type == ONLINE:
        point_class = OnReaction
    else:
        point_class = OffReaction
    reaction = point_class.create(
        text=text,
        point_num=point_num,
        order_num=order_num)
    return reaction

@exception_guard
def get_reaction_with_point(point_num, order_num):
    if MODE == ONLINE:
        reaction_class = OnReaction
    else:
        reaction_class = OffReaction
    reaction = reaction_class.get((reaction_class.point_num == point_num) & (reaction_class.order_num == order_num))
    return reaction

@exception_guard
def get_answer_reaction(chat_id, result):
    return get_reaction_with_point(view.point.cur_point(chat_id).id, result)

###

@exception_guard
def get_reaction_with_id(id):
    if MODE == ONLINE:
        reaction_class = OnReaction
    else:
        reaction_class = OffReaction
    reaction = reaction_class.select().where(reaction_class.id == id).get()
    return reaction

@exception_guard
def delete_reaction(id):
    reaction = get_reaction_with_id(id)
    reaction.delete_instance()