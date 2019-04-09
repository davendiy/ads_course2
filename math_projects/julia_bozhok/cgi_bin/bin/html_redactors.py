#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Модуль з функціями, які змінюють html сторінки
"""

from .constants import *


def showerror(message):
    """ Вивести html сторінку з помилкою на екран

    :param message: повідомлення
    """
    with open(ERROR_PAGE, 'r', encoding='utf-8') as file:
        page = file.read().format(message=str(message))
    print(change_html(page, mode=STRING_MODE))


def showhref(path, message):
    """ Показати сторінку з посиланням на файл

    :param path: шлях до файлу, або просто посилання
    :param message: текст, який буде посиланням
    """
    with open(FINAL_PAGE, 'r', encoding='utf-8') as file:
        page = file.read().format(message=str(message), href=path)
    print(change_html(page, mode=STRING_MODE))


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
    with open(STYLE_SHEET, 'r', encoding='utf-8') as file:
        style = file.read()

    style = '<style>' + style + '</style>'
    text = text.replace('<link rel="stylesheet" href="style.css">', style)

    text = text.replace('home_page.html', '../front/home_page.html')
    text = text.replace('add_page.html', '../front/add_page.html')
    return text


def fill_cr_page(page: str, list_values: list) -> str:
    """ Додати в html текст рядки таблиці

    В html паттерні сторінки (revenue_page_pattern.html i costs_page_pattern.html)
    таблиця з результатми містить тільки заголоки, після яких стоїть коментар <!-- {} -->
    замість цього коментаря необхідно вставити код, який імплементуватиме рядок таблиці

    :param page: рядок з html кодом, в якому наявний '<!-- {} -->'
    :param list_values: [{"Sum": ...,
                          "Id": ...,
                          "Category: ...,
                          "Date": ...,
                          "Comments": ...}] - список словників, які повертає BudgetCollection
    :return:
    """
    tmp = ''
    for el in list_values:
        tmp += HTML_PIECE.format(**el)         # формуємо послідовність рядків таблиці
    return page.format(tmp)
