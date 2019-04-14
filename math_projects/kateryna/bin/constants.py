#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import logging

DEFAULT_N = 100    # к-ть елементів, які повертає пошук за умовчанням

# типи елементів (значення - назви таблиць у БД)
KEY_WORD = 'Key_words'
SITE = 'Sites'
LINK = 'Links'

# назва таблиці категорій
CATEGORIES = 'Categories'

DEFAULT_DATABASE = 'data.db'

DEFAULT_LOG_CLIENT = 'parser_client.log'
FORMAT = '%(asctime) -15s %(message)s'  # формат запису: <час> <повідомлення>

DEFAULT_LOG_GUI = 'parser_gui.log'

SLEEP = 1

# списки полів для кожної таблиці
LINKS_GUI_FIELDS = ['Link', 'Category', 'Date', 'Information']


SITES_GUI_FIELDS = ['Id', 'Name', 'Link']
KEY_WORDS_GUI_FIELDS = ['Id', 'Word']

SITES_DATA_FIELDS = ['Id', 'Name', 'Link', 'Category_id']
KEY_WORDS_DATA_FIELDS = ['Id', 'Word', "Category_id"]

CATEGORIES_FIELDS = ['Id', 'Name']

logging.basicConfig(filename=DEFAULT_LOG_GUI, format=FORMAT, level=logging.DEBUG)
