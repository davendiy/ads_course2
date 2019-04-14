#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import logging

DEFAULT_N = 1000    # к-ть елементів, які повертає пошук за умовчанням

# типи елементів (значення - назви таблиць у БД)
KEY_WORD = 'Key_words'
SITE = 'Sites'
LINK = 'Links'

CATEGORIES = 'Categories'     # назва таблиці категорій

DEFAULT_DATABASE = 'data.db'  # шлях до бд за умовчанням

DEFAULT_LOG_GUI = 'parser_gui.log'      # файл з логами для графічного інтерфейсу
DEFAULT_LOG_CLIENT = 'parser_client.log'    # файл з логами для клієнта
FORMAT = '%(asctime) -15s %(message)s'  # формат запису: <час> <повідомлення>

SLEEP = 1  # тривалість інтервалу монтіорингу (у годинах)

# списки полів для кожної таблиці, які відображаються
LINKS_GUI_FIELDS = ['Link', 'Category', 'Date', 'Information']
SITES_GUI_FIELDS = ['Id', 'Name', 'Link']
KEY_WORDS_GUI_FIELDS = ['Id', 'Word']

# списки всіх полів для кожної таблиці
SITES_DATA_FIELDS = ['Id', 'Name', 'Link', 'Category_id']
KEY_WORDS_DATA_FIELDS = ['Id', 'Word', "Category_id"]
CATEGORIES_FIELDS = ['Id', 'Name']
