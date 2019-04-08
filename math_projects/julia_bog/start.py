#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from http.server import HTTPServer, CGIHTTPRequestHandler
import datetime

# необхідно змінити cgi-bin на cgi_bin щоб можна було імпортувати пакет з цієї папки
CGIHTTPRequestHandler.cgi_directories = ['/cgi_bin', '/htbin']

HOST = ''               # Комп'ютер для з'єднання
PORT = 8001             # Порт для з'єднання

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/home_page.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
