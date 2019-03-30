#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t27_01_local_webserver.py
# Локальний веб-сервер

# TODO дохрена ше нада всього зробити
# TODO зробити темплейти таблиць на хтмл сторінках так, щоб скрипт міг
# TODO додавати записи.

# TODO між хтмл сторінками переходим по ссилкам, щоб зробити якісь зміни - формуємо запрос
# TODO также нада додати діалогові сторінки, а ето жопа. ВЕРНІТЬ ПОЖАЛУСТА GUI

from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = ''               # Комп'ютер для з'єднання
PORT = 8000             # Порт для з'єднання

print('=== Local webserver ===')
print("стартова сторінка:", "http://localhost:{}/front/home_page.html".format(PORT))
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
