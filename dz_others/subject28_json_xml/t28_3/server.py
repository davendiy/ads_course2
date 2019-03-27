#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# Локальний веб-сервер

from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ''               # Комп'ютер для з'єднання
PORT = 8000             # Порт для з'єднання

print('=== Local webserver ===')
print('start page: http://localhost:{}/open_page28_3.html'.format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
