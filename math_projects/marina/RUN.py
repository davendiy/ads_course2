#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from http.server import HTTPServer, CGIHTTPRequestHandler
from cgi_bin.sceleton import *
import pickle

# необхідно змінити cgi-bin на cgi_bin щоб можна було імпортувати пакет з цієї папки
CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

logging.debug('STARTED')
HOST = ''               # Комп'ютер для з'єднання
PORT = 8002             # Порт для з'єднання

print(database.get_items('Update'))

with open(SESSIONS_URL, 'wb') as file:
    pickle.dump({}, file)

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/login.html".format(PORT))
print("ADMIN PARAMS\nlogin: admin\npassword: 1234")

print('\nUSER PARAMS\nlogin: test user\npassword: test')
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
