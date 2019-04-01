#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from .structure import *
import datetime


form = cgi.FieldStorage()

with open('logs.log', 'a') as file:
    file.write('\n\n')
    file.write(str(form) + '\n')

if REVENUE in form or COST in form:

    item_type = REVENUE if REVENUE in form else COST
    fields = REVENUE_FIELDS if REVENUE in form else COSTS_FIELDS

    # виведення сторінки для введення параметрів
    if START_ADDING == form[item_type].value:
        with open(DIALOG_REC_PATTERN, 'r', encoding='utf-8') as file:
            page = file.read()
        date = str(datetime.datetime.now().date())
        page = page.format(cur_date=date, type=item_type)
        print(change_html(page, mode=STRING_MODE))
        exit(0)

    # приймання параметрів з попередньої сторінки
    else:

        # пробуємо зчитати всі необхідні параметри
        try:
            params = {name: form[name].value for name in fields if name != COMMENTS and name != 'id'}
        except KeyError:
            showerror('Please, fill all the fields (Comments - optional)')
            exit(1)

        if COMMENTS in form:
            params[COMMENTS] = form[COMMENTS].value
        else:
            params[COMMENTS] = ''

        # якщо введеної категорії не існує, то додаємо таку до бази даних
        translator = name_dict(data_connector.get_categories(item_type))
        if params['Category'] not in translator:
            data_connector.add_category(params['Category'], item_type)
            translator = name_dict(data_connector.get_categories(item_type))

        # перетворюємо Category в Category_id
        params['Category_id'] = translator[params['Category']]
        del params['Category']

        # перевіряємо формат дати
        tmp = params['Date'].split('-')
        if len(tmp) != 3 or any([not tmp[0].isdigit(), not tmp[1].isdigit(), not tmp[2].isdigit()]):
            showerror("Please, enter the date in format yyyy.mm.dd")
            exit(1)

        params['item_type'] = item_type
        # завдяки тому, що імена змінних і параметрів в таблиці однакові можна використати **
        data_connector.add_item(**params)

        # оновлюємо сторінки і виводимо відповідно сторінку витрат, або доходів
        year, month, day = str(datetime.datetime.now().date()).split('-')
        update_cr_pages(item_type=item_type)
        update_home_page(year, month, day)

        if item_type == REVENUE:
            print(change_html(REVENUE_PAGE, mode=FILE_MODE))
        else:
            print(change_html(COSTS_PAGE, mode=FILE_MODE))
