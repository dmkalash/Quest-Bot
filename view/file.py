# -*- coding: utf-8 -*-

from models import File
from exception_guard import exception_guard

@exception_guard
def add_file(file_id, point_num, order_num, file_type):
    file = File.create(
        file_id=file_id,
        point_num=point_num,
        order_num=order_num,
        file_type=file_type)
    return file

'''
@exception_guard
def add_file(**kwargs):
    file = File.create(**kwargs)
    return file
'''

@exception_guard
def get_files_with_point(point):
    query = (File.select().where(File.point == point).order_by(File.order_num))
    return query

####

@exception_guard
def get_file_with_id(file_id):
    file = File.get(File.file_id == file_id)
    return file

@exception_guard
def delete_file(id):
    point = get_file_with_id(id)
    point.delete_instance()
