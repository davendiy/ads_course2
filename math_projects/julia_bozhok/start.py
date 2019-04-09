#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Головна програма, яка запускає сервер і виводить
посилання на домашню сторінку
"""

from http.server import HTTPServer, CGIHTTPRequestHandler
from cgi_bin.bin import *

# необхідно змінити cgi-bin на cgi_bin щоб можна було імпортувати пакет з цієї папки
CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання

# оновлюємо домашню сторінку значеннями з бази даних
data = data_connector.find_item('')
categories = data_connector.get_categories()
translator = id_dict(categories)
for el in data:
    el['Category'] = translator[el['Category_id']]
    del el['Category_id']

with open(HOME_PAGE_PATTERN, 'r', encoding='utf-8') as file:
    page = file.read()

page = fill_cr_page(page, data)
with open(HOME_PAGE, 'w', encoding='utf-8') as file:
    file.write(page)

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/home_page.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
