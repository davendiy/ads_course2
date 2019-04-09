#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Скрипт, який оновлює домашню сторінку, коли нажимають кнопку Find!

Також має обробити варіант, коли користувач нажимає кнопку Release - вивести сторінку
з вибраним елементом
"""

from bin import *
import cgi

form = cgi.FieldStorage()

# обробка кнопки Release
if START_RELEASE in form:
    if 'Id' not in form:        # необхідно, щоб був заповнений id
        showerror('Please, enter the id')
        exit(1)
    item = data_connector.get_item(form['Id'].value)

    with open('logs.log', 'a') as file:   # логи
        file.write(f'\n\nitem for release: {item}\n\n')

    if not item:        # перевірка чи є елемент з таким ід
        showerror('There is no item with such id')
        exit(1)

    # заміна назви категорії на id
    item['Category'] = data_connector.find_category_name(item['Category_id'])
    del item['Category_id']
    with open(RELEASE_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()

    # через те, що назви полів і ключових змінних однакові - можна використовувати **
    page = page.format(**item)
    print(change_html(page, mode=STRING_MODE))
    exit(0)

# обробка кнопки Find! (необхідно, щоб хоч один з параметрів був у формі)
if any([param in form for param in HOME_PARAMS]):

    # якщо користувач ввів частину імені, або назву категорії - зчитуємо ці значення
    name = '' if 'Name' not in form else form['Name'].value
    category = '' if 'Category' not in form else form['Category'].value
    category_id = ''

    if category:    # якщо введена категорія - шукаємо її id
        category_id = data_connector.find_category_id(category)

    # пошук всіх елементів, які задовольняють введеним параметрам
    result = data_connector.find_item(piece_of_name=name, category=category_id)
    with open(HOME_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()

    # замінюємо в кожному елементі код категорії на її назву
    categories = data_connector.get_categories()
    translator = id_dict(categories)
    for el in result:
        el['Category'] = translator[el['Category_id']]
        del el['Category_id']

    page = fill_cr_page(page, result)   # змінюємо і виводимо сторінку

    print(change_html(page, mode=STRING_MODE))
