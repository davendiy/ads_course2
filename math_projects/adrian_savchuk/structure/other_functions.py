#!/usr/bin/env python3
# -*-encoding: utf-8-*-


REVENUE_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')
COSTS_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

DEFAULT_N = 40
REVENUE = 'Revenues'
COST = 'Costs'
DEFAULT_CONFIG_FILE = 'config.bud'
DEFAULT_DATABASE = './budget.db'


def name_dict(dicts_list) -> dict:
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
