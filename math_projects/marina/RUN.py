#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# TODO DEBUG
# TODO modify login page, add css
# TODO add comments
# TODO refactor

from http.server import HTTPServer, CGIHTTPRequestHandler
from cgi_bin.sceleton import *
import pickle

# необхідно змінити cgi-bin на cgi_bin щоб можна було імпортувати пакет з цієї папки
CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

logging.debug('STARTED')
HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання

with open(SESSIONS_URL, 'wb') as file:
    pickle.dump({}, file)

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/login.html".format(PORT))
print("ADMIN PARAMS\nlogin: admin\npassword: 1234")

HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
