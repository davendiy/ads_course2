#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Модуль з додатковими функціями.
"""

# поля у вікні випуску товару
ROWS_DIALOG = ('id', 'Department_id', 'Build_number', 'Shelf_number')

# розмір частинки, якими копіюється файл
CHUNK = 1024 * 100

# поля у головному вікні
ROWS_MAIN = ('id', 'Name', 'Category', 'Department_id', 'Build_number', 'Shelf_number')


def name_dict(dicts_list):
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {Name: id}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(Name1: id1, Name2: id2)
    """
    res = {}
    for el in dicts_list:
        res[el['Name']] = el['id']
    return res


def id_dict(dicts_list):
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {id: Name}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(id1: Name1, id2: Name2)
    """
    res = {}
    for el in dicts_list:
        res[el['id']] = el['Name']
    return res
