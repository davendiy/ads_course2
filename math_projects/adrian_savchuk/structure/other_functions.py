#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Список полів з таблиці REVENUE, які будуть відображатись у GUI
REVENUE_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

# Список полів з таблиці COST, які будуть відображатись у GUI
COSTS_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

# К-ть елементів за умовчанням, які буде видавати пошук
DEFAULT_N = 40

# Константа, що означає тип транзакції 'Дохід'. Збігається з назвою таблиці з доходами
REVENUE = 'Revenues'

# Константа, що означає тип транзакції 'Витрата'. Збігається з назвою таблиці з витратами
COST = 'Costs'

# шлях за умовчанням до бази даних
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
