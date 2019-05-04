#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from .sceleton import *
import random
import pickle

form = cgi.FieldStorage()


if 'login' and 'password' in form:
    login = form['login'].value
    password = form['password'].value
    hashed = database.get_user_pass(login)   # перевірка пароля
    if check_pass(password, hashed):

        with open(SESSIONS_URL, 'rb') as file:
            sessions = pickle.load(file)

        cur_session = random.randint(0, 100500)   # створення унікального id для кожного користувача, що заходить на сайт
        sessions[cur_session] = login             # запис його в словник користувачів
        with open(SESSIONS_URL, 'wb') as file:
            pickle.dump(sessions, file)

        if login == ADMIN:
            page = change_html(ADMIN_PAGE_PATTERN, FILE_MODE)
            page = page.format(session=cur_session)
            print(page)
        else:
            page = change_html(CART_PAGE_PATTERN, FILE_MODE)
            page = page.format(session=cur_session)
            print(page)
    else:
        page = change_html(LOGIN_PAGE, FILE_MODE)
        page = page.replace(FORMAT_PLACE, HTML_WRONG_PASS)
        print(page)
