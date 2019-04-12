#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from math_projects.kateryna.bin import *
import datetime
import logging
from time import sleep

# логування
logging.basicConfig(filename=DEFAULT_LOG_CLIENT, format=FORMAT, level=logging.DEBUG)


def create_pattern(listdicts):
    """ Створити регулярний вираз за списком словників, що видає БД
    """
    pattern = ''
    for el in listdicts:
        pattern += '|' + el['Word']
    return pattern.strip('|')


def monitoring():
    """ Функція, що здійснює моніторинг заданих сайтів з бази даних
    """
    categories = id_dict(database.get_categories())     # словник категорій
    logging.info('\n\nStarting parse...\n\n')
    now = str(datetime.datetime.now())              # поточний датачас

    # проходимо по категоріях і для кожної моніторимо відповідні сайти за відповідними ключовими словами
    for cat_id in categories:
        logging.info('\n\n------------------------Category: {}----------------------------'.format(categories[cat_id]))
        sites = database.get_items(item_type=SITE, category=cat_id)         # всі сайти для даної категорії
        key_words = database.get_items(item_type=KEY_WORD, category=cat_id)   # ключові слова для даної категорії
        pattern = re.compile(create_pattern(key_words))         # шаблон ключових слів

        logging.info('pattern = {}'.format(pattern))
        for site in sites:                           # проходимо по всіх сайтах і кожен парсимо
            url = site['Link']
            logging.info('site: {}'.format(url))
            links = parse_page(url, pattern)

            for link, _text in links.items():      # результати пошуку додаємо до бази даних
                database.add_item(item_type=LINK,
                                  Link=link,
                                  Category_id=cat_id,
                                  Date=now,
                                  Information=_text,
                                  )
                logging.info('added {} because of {}'.format(link, _text))
    logging.info('successful\n====================================================================================\n\n')


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        sleeptime = int(SLEEP * 3600)
    else:
        sleeptime = int(sys.argv[1] * 3600)

    while True:         # моніторинг з певним періодом
        print('starting parse...')
        try:
            monitoring()
            print('successful')
        except Exception as e:
            logging.exception(e)
            print('ends')
        sleep(sleeptime)
