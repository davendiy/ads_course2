#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from math_projects.alexandra.cgi_bin.structure import *
import cgi
import datetime

# зчитуємо форму, яка надсилається
form = cgi.FieldStorage()

# якщо хоч один параметр з необхідних присутній, то змінюємо сторінку
if any([param in form for param in POST_PARAMS]):

    chosen_type = ''    # за день, за місяць, за рік або а весь час

    # вибрана категорія
    chosen_category = form['Category'].value if 'Category' in form else ''
    for param in POST_PARAMS:     # шукаємо, який тип є у формі  (Day, Month, Year або All_time
        if param == 'Category':
            continue
        if param in form:
            chosen_type = param
            break

    # зчитуємо всі записи
    items = data_connector.get_items(item_type=REVENUE, category=chosen_category)

    year, month, day = str(datetime.datetime.now().date()).split('-')

    # словник {"Category_name": "Category_id"}
    translator = id_dict(data_connector.get_categories(item_type=REVENUE))

    result = []      # відсіюємо ті, які не підходять
    for el in items:
        el['Category'] = translator[el['Category_id']]
        del el['Category_id']
        tmp_year, tmp_month, tmp_day = el['Date'].split('-')
        if chosen_type == 'Day' and any([tmp_year != year, tmp_month != month, tmp_day != day]):
            continue
        if chosen_type == 'Month' and (tmp_year != year or tmp_month != month):
            continue
        if chosen_type == 'Year' and (tmp_year != year):
            continue

        result.append(el)

    # заповнюємо html сторінку і виводимо її
    with open(REVENUE_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        tmp = file.read()

    res_page = fill_cr_page(tmp, result)

    with open(REVENUE_PAGE, 'w', encoding='utf-8') as file:
        file.write(res_page)

    print(change_html(REVENUE_PAGE))
