#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from bin import *
import cgi

form = cgi.FieldStorage()

if END_RELEASE in form:
    with open('logs.log', 'a') as file:
        file.write(f'\n\nrelease form: {form}')
    data = {param: form[param].value for param in RELEASE_PARAMS}
    data_connector.delete_item(data['id'])
    data['Category_id'] = data_connector.find_category_id(data['Category'])
    create_report(DEFAULT_REPORT, REPORT_TEMPLATE, [data])

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

    showhref('../' + DEFAULT_REPORT, "download report")
