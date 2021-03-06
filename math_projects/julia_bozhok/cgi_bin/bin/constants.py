#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Глобальні константи та деякі додаткові функції.
"""

AUTHOR = 'Божок Юлія'

# шляхи до html сторінок
HOME_PAGE = 'front/home_page.html'
RELEASE_PAGE = 'front/release_page.html'
FINAL_PAGE = 'front/final.html'
ERROR_PAGE = 'front/error_page.html'

# шляхи до шаблонів html сторінок
HOME_PAGE_PATTERN = 'front/home_page_pattern.html'
ADD_PAGE_PATTERN = 'front/add_page.html'
RELEASE_PAGE_PATTERN = 'front/release_page_pattern.html'

STYLE_SHEET = 'front/style.css'        # шлях до css файлу

# К-ть елементів за умовчанням, які буде видавати пошук
DEFAULT_N = 40

# шляхи за умовчанням
DEFAULT_DATABASE = 'storage.db'    # до бази даних
DEFAULT_REPORT = 'report.docx'     # до файлу, в якому буде зберігатись звіт
REPORT_TEMPLATE = 'template.docx'  # до шаблону звіту

# Назва тимчасового exel файлу
TMP_FILE_NAME = '___tmp.xlsx'

# параметри, які надсилають сторінки через метод POST
ADD_PARAMS = ['Name', 'Category', 'Build_number', 'Department_id', 'Shelf_number']
HOME_PARAMS = ['Name', "Category", 'Find!']
RELEASE_PARAMS = ['id', 'Name', 'Category', 'Build_number', 'Department_id', 'Shelf_number']

# додаткові параметри методу POST, які визначають режим роботи
START_RELEASE = 'Start'
END_RELEASE = 'End'
CANCEL_RELEASE = 'Cancel'

# html опис рядка таблиці
HTML_PIECE = """
            <tr>
                <td>{id}</td>
                <td>{Name}</td>
                <td>{Category}</td>
                <td>{Department_id}</td>
                <td>{Build_number}</td>
                <td>{Shelf_number}</td>
            </tr>
"""

FILE_MODE = 'file'      # параметри функцій з html_redactors, які визначають режим,
STRING_MODE = 'string'  # в якому змінюється сторінка


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
