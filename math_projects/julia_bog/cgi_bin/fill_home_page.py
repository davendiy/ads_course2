#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from bin import *
import cgi

form = cgi.FieldStorage()

if any([param in form for param in HOME_PARAMS]):
    name = '' if 'Name' not in form else form['Name'].value
    category = '' if 'Category' not in form else form['Category'].value

    if category:
        category = data_connector.find_category_id(category)

    result = data_connector.find_item(piece_of_name=name, category=category)
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
