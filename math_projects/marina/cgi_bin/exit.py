#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""CGI скрипт обробки натиснення на кнопу SIGN_OUT

Завершує сесію
"""

import cgi
from sceleton import *
import pickle


form = cgi.FieldStorage()

if 'Exit' in form:
    cur_session = form['session'].value if 'session' in form else ''
    with open(SESSIONS_URL, 'rb') as file:
        sessions = pickle.load(file)

    if cur_session in sessions:
        del sessions[cur_session]

    with open(SESSIONS_URL, 'wb') as file:
        pickle.dump(sessions, file)

    page = change_html(LOGIN_PAGE, FILE_MODE)
    print(page)
