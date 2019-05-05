#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import bcrypt
import logging

logging.basicConfig(filename='logs.log', format='%(asctime) -15s %(message)s', level=logging.DEBUG)


def encrypt(password, encoding='utf-8'):
    return bcrypt.hashpw(bytes(password, encoding=encoding), bcrypt.gensalt(14))


def check_pass(password, hashed, encoding='utf-8'):
    return bcrypt.checkpw(bytes(password, encoding=encoding), hashed)


def name_dict(dicts_list) -> dict:
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {Name: id}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(Name1: id1, Name2: id2)
    """
    res = {}
    for el in dicts_list:
        res[el['Name']] = el['Id']
    return res


def id_dict(dicts_list):
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {id: Name}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(id1: Name1, id2: Name2)
    """
    res = {}
    for el in dicts_list:
        res[el['Id']] = el['Name']
    return res