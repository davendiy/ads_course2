#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# import sys
# import os
# sys.path.insert(0, '/files/univer/python/course2/math_projects/alexandra/structure')

from structure import *
import cgi


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

    update_cr_pages(chosen_category=chosen_category, item_type=COST, chosen_type=chosen_type)
    print(change_html(COSTS_PAGE))
