#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t27_01_local_webserver.py
# Локальний веб-сервер

# TODO зробити python діалоги додавання і видалення

from http.server import HTTPServer, CGIHTTPRequestHandler
from cgi_bin.structure import *
import datetime

CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання

chosen_category = ''

year, month, day = str(datetime.datetime.now().date()).split('-')

update_cr_pages(item_type=COST)
update_home_page(year, month, day)

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/home_page.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
