#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from structure import *
import datetime


def save():
    try:
        params = {name: form[name].value for name in fields if name != COMMENTS and name != 'id'}
    except KeyError:
        showerror('Please, fill all the fields (Comments - optional)')
        return 1
    if COMMENTS in form:
        params[COMMENTS] = form[COMMENTS].value
    else:
        params[COMMENTS] = ''

    translator = name_dict(data_connector.get_categories(item_type))
    if params['Category'] not in translator:
        data_connector.add_category(params['Category'], item_type)
        translator = name_dict(data_connector.get_categories(item_type))

    params['Category_id'] = translator[params['Category']]
    del params['Category']

    tmp = params['Date'].split('-')
    if len(tmp) != 3 or any([not tmp[0].isdigit(), not tmp[1].isdigit(), not tmp[2].isdigit()]):
        showerror(ErrorBadDate)
        return 1

    params['item_type'] = item_type
    data_connector.add_item(**params)

    year, month, day = str(datetime.datetime.now().date()).split('-')
    update_cr_pages(item_type=item_type)
    page = update_home_page(year, month, day)

    if item_type == REVENUE:
        print(change_html(REVENUE_PAGE, mode=FILE_MODE))
    else:
        print(change_html(COSTS_PAGE, mode=FILE_MODE))
        # print(change_html(page, mode=STRING_MODE), end='')



form = cgi.FieldStorage()

with open('logs.log', 'a') as file:
    file.write('\n\n')
    file.write(str(form) + '\n')
    # file.write(str(form[item_type].value) + '\n')
    # file.write(str(form[item_type]))

if REVENUE in form or COST in form:

    item_type = REVENUE if REVENUE in form else COST
    fields = REVENUE_FIELDS if REVENUE in form else COSTS_FIELDS
    #
    # with open('logs.log', 'a') as file:
    #     file.write('\n\n')
    #     file.write(str(form)+'\n')
    #     file.write(str(form[item_type].value) + '\n')
    #     file.write(str(form[item_type]))

    if START_ADDING == form[item_type].value:
        with open(DIALOG_REC_PATTERN, 'r', encoding='utf-8') as file:
            page = file.read()
        date = str(datetime.datetime.now().date())
        page = page.format(cur_date=date, type=item_type)
        print(change_html(page, mode=STRING_MODE))
        exit(0)
    else:
        save()
        exit(0)
