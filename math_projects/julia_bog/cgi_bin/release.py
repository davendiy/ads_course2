#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Скрипт, який обробляє сторінку з відпуском товару.
"""

from bin import *
import cgi
import datetime

form = cgi.FieldStorage()


# обробка натиснення кнопки Release
if END_RELEASE in form:
    with open('logs.log', 'a') as file:   # логи
        file.write(f'\n\nrelease form: {form}')

    # формуємо словник з параметрів
    data = {param: form[param].value for param in RELEASE_PARAMS}
    data_connector.delete_item(data['id'])   # видаляємо елемент з бази даних
    # змінюємо назву категорії на її ід
    data['Category_id'] = data_connector.find_category_id(data['Category'])

    data['cur_date'] = str(datetime.datetime.now().date())
    data['author'] = AUTHOR

    with open('logs.log', 'a', encoding='utf-8') as file:
        file.write(f'\n\nreport parameters: {data}\n\n')
    create_report(DEFAULT_REPORT, REPORT_TEMPLATE, [data])   # створюємо звіт за шаблоном

    # оновлюємо домашню сторінку
    with open(HOME_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()

    data = data_connector.get_items()
    categories = data_connector.get_categories()
    translator = id_dict(categories)
    for el in data:
        el['Category'] = translator[el['Category_id']]
        del el['Category_id']

    page = fill_cr_page(page, data)
    with open(HOME_PAGE, 'w', encoding='utf-8') as file:
        file.write(page)

    # виводимо сторінку з посиланням на звіт
    showhref('../' + DEFAULT_REPORT, "download report")
