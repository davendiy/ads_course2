#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# todo: change constants
# todo: config find
# todo: add backend for dialogs for adding new item
# todo: don't forget to review comments
# todo: remove redundant functions
# todo: config report
# todo: maybe add the number of items to dialog and modify the search to except repeats

from http.server import HTTPServer, CGIHTTPRequestHandler
import datetime
from .cgi_bin.bin import *

# необхідно змінити cgi-bin на cgi_bin щоб можна було імпортувати пакет з цієї папки
CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання


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
