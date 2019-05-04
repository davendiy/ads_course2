#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# TODO modify login page, add css
# TODO complete database
# TODO add backend for each html page
# TODO add comments
# TODO refactor

from http.server import HTTPServer, CGIHTTPRequestHandler

# необхідно змінити cgi-bin на cgi_bin щоб можна було імпортувати пакет з цієї папки
CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/login.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
