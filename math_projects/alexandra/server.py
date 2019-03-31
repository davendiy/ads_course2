#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t27_01_local_webserver.py
# Локальний веб-сервер

# TODO зробити python діалоги додавання і видалення
# TODO зробити діаграму

from http.server import HTTPServer, CGIHTTPRequestHandler
from cgi_bin.structure import *
import datetime

CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання

chosen_category = ''

# ------------------------------- підготовка сторінки витрат -----------------------------------------

# зчитуємо всі записи
items = data_connector.get_items(item_type=COST, category=chosen_category)
print(items)
year, month, day = str(datetime.datetime.now().date()).split('-')

# словник {"Category_name": "Category_id"}
translator = id_dict(data_connector.get_categories(item_type=COST))

for el in items:
    el['Category'] = translator[el['Category_id']]
    del el['Category_id']
# заповнюємо html сторінку і виводимо її
with open(COSTS_PAGE_PATTERN, 'r', encoding='utf-8') as file:
    tmp = file.read()

res_page = fill_page(tmp, items)

with open(COSTS_PAGE, 'w', encoding='utf-8') as file:
    file.write(res_page)


# ------------------------------- підготовка сторінки доходів -----------------------------------------
# зчитуємо всі записи
items = data_connector.get_items(item_type=REVENUE, category=chosen_category)

year, month, day = str(datetime.datetime.now().date()).split('-')

# словник {"Category_name": "Category_id"}
translator = id_dict(data_connector.get_categories(item_type=REVENUE))

for el in items:
    el['Category'] = translator[el['Category_id']]
    del el['Category_id']

# заповнюємо html сторінку і виводимо її
with open(REVENUE_PAGE_PATTERN, 'r', encoding='utf-8') as file:
    tmp = file.read()

res_page = fill_page(tmp, items)

with open(REVENUE_PAGE, 'w', encoding='utf-8') as file:
    file.write(res_page)

# ------------------------------- підготовка домашньої сторінки -----------------------------------------

with open(HOME_PAGE_PATTERN, 'r', encoding='utf-8') as file:
    page = file.read()

page = fill_home(page, costs_day=data_connector.get_sum(year=year, month=month, day=day, item_type=COST),
                 costs_month=data_connector.get_sum(year=year, month=month, item_type=COST),
                 revenue_month=data_connector.get_sum(year=year, month=month, item_type=REVENUE),
                 balance=data_connector.balance)
with open(HOME_PAGE, 'w', encoding='utf-8') as file:
    file.write(page)


print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/home_page.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
