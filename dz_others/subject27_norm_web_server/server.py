#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t27_01_local_webserver.py
# Локальний веб-сервер

from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ''               # Комп'ютер для з'єднання
PORT = 8000             # Порт для з'єднання

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/t27_4_open_page.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
