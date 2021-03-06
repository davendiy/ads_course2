#!/usr/bin/env python3
# -*-encoding: utf-8-*-


from .database import *
from .other_functions import *


def change_html(filename_or_page, mode=FILE_MODE):
    """ Прочитати html сторінку і змінити її у формат,
    який буде надсилати cgi скрипт

    :param filename_or_page: назва файлу
    :param mode: вказує в якому режимі працює функція: FILE_MODE - на вхід дано назву файлу
                                                       STRING_MODE - на вхід дано рядок
    :return: рядок
    """

    # замінюємо <!DOCTYPE html> на Content-type: text/html charset=utf-8\n\n
    if mode == FILE_MODE:
        with open(filename_or_page, 'r', encoding='utf-8') as file:
            text = file.read().strip()
    else:
        text = filename_or_page
    text = text.replace('<!DOCTYPE html>', 'Content-type: text/html charset=utf-8\n\n')

    # вставляємо в <head> замість <link rel="stylesheet" href="style.css"> дані з css файла
    with open(STYLESHEET, 'r', encoding='utf-8') as file:
        style = file.read()

    style = '<style>' + style + '</style>'
    text = text.replace('<link rel="stylesheet" href="./main.css">', style)

    text = text.replace('admin.html', '../front/admin.html')
    text = text.replace('addition.html', '../front/addition.html')
    text = text.replace('cart.html', '../front/cart.html')
    return text


def fill_page(page_or_filename, data, mode=FILE_MODE, button_template=''):
    """ Наповнити html сторінку інформацією з бази даних

    :param page_or_filename: сторінка, або шлях до сторінки
    :param data: список словників, які необхідно буде вставити
    :param mode: режим, в якому працює функція: FILE_MODE - на вхід дано назву файлу
                                                STRING_MODE - на вхід дано рядок
    :param button_template: BUTTON_AND or BUTTON_DELETE - шаблон кнопки, що буде вставлятись
    :return: змінений текст сторінки
    """
    logging.debug('template button: {}'.format(button_template))
    page = page_or_filename
    if mode == FILE_MODE:
        with open(page_or_filename, 'r', encoding='utf-8') as file:
            page = file.read()

    with open(PRODUCT_PATTERN, 'r', encoding='utf-8') as file:
        template = file.read()

    res = ''
    translate = id_dict(database.get_categories())
    logging.debug('translate: {}'.format(translate))
    summary = 0
    flag = data and 'Price' in data[0]
    for el in data:                               # створення списку товарів
        tmp_el = el.copy()
        tmp_el["Category"] = translate[int(tmp_el['Category_id'])]
        button = button_template.replace("{Item_id}", str(tmp_el['Id']))
        del tmp_el['Category_id']
        del tmp_el['Id']
        tmp_el['Button'] = button
        if flag:
            summary += float(el['Price'])
        # можна використовувати ** завдяки тому, що назви полів і ключові параметри однакові
        res += template.format(**tmp_el)
    res += FORMAT_PLACE  # про всяк випадок, може знадобиться потім ще додавати елементи

    page = page.replace(FORMAT_PLACE, res)  # вставляємо шматок коду в замість коментаря
    page = page.replace('{Sum}', str(summary))
    return page


def create_home_page(page_path, cur_session, button_template, category=''):
    """ Створити домашню сторінку для користувача / адміна

    :param page_path: шлях до шаблону сторінки
    :param cur_session: ід сесії
    :param button_template: шаблон кнопки
    :param category: категорія, за якою шукаються елементи
    :return: html сторінка
    """
    page = change_html(page_path, FILE_MODE)
    page = page.replace('{session}', cur_session)
    data = database.get_items(category)
    logging.debug('data for home page: {}'.format(data))
    page = fill_page(page, data, mode=STRING_MODE, button_template=button_template)
    return page


def create_cart_page(page_path, cur_session, button_template, user_id):
    """ Створити сторінку корзини для користувача

    :param page_path: шлях до шаблону
    :param cur_session: ід сесії
    :param button_template: шаблон кнопки
    :param user_id: ід користувача
    :return: html сторінка
    """
    page = change_html(page_path, FILE_MODE)
    page = page.replace('{session}', cur_session)
    tmp_data = database.get_cart(user_id)
    data = []
    for el in tmp_data:
        data.append(database.get_one_item(el['Item_id']))
    logging.debug('data for cart page: {}'.format(data))
    page = fill_page(page, data, mode=STRING_MODE, button_template=button_template)
    print(page)