#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from bin import *
import cgi

form = cgi.FieldStorage()


if START_RELEASE in form:
    if 'Id' not in form:
        showerror('Please, enter the id')
        exit(1)
    item = data_connector.get_item(form['Id'].value)
    with open('logs.log', 'a') as file:
        file.write(f'\n\nitem for release: {item}\n\n')
    if not item:
        showerror('There is no item with such id')
        exit(1)

    item['Category'] = data_connector.find_category_name(item['Category_id'])
    del item['Category_id']
    with open(RELEASE_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()
    page = page.format(**item)
    print(change_html(page, mode=STRING_MODE))
    exit(0)


if any([param in form for param in HOME_PARAMS]):
    name = '' if 'Name' not in form else form['Name'].value
    category = '' if 'Category' not in form else form['Category'].value
    category_id = ''

    if category:
        category_id = data_connector.find_category_id(category)

    result = data_connector.find_item(piece_of_name=name, category=category_id)
    with open(HOME_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()

    categories = data_connector.get_categories()
    translator = id_dict(categories)
    for el in result:
        el['Category'] = translator[el['Category_id']]
        del el['Category_id']

    page = fill_cr_page(page, result)

    with open(HOME_PAGE, 'w', encoding='utf-8') as file:
        file.write(page)

    print(change_html(page, mode=STRING_MODE))
