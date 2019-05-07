#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from sceleton import *
import random
import pickle

form = cgi.FieldStorage()

logging.debug(str(form))
if 'Sign_in' in form:
    login = form['login'].value if 'login' in form else ''
    password = form['password'].value if 'password' in form else ''
    hashed = database.get_user_pass(login)   # перевірка пароля
    if check_pass(password, hashed) and login and password:
        logging.debug('PASSWORD CHECKED')
        with open(SESSIONS_URL, 'rb') as file:
            sessions = pickle.load(file)

        cur_session = str(random.randint(0, 100500))  # створення унікального id для кожного користувача, що заходить на сайт
        sessions[cur_session] = database.get_user_id(login)     # запис його в словник користувачів
        with open(SESSIONS_URL, 'wb') as file:
            pickle.dump(sessions, file)

        if login == ADMIN:
            page = change_html(ADMIN_PAGE_PATTERN, FILE_MODE)
            page = page.replace('{session}', cur_session)
            data = database.get_items()
            page = fill_page(page, data, STRING_MODE)
            # logging.debug(page)
            print(page)
        else:
            page = change_html(HOME_USER_PAGE_PATTERN, FILE_MODE)
            page = page.replace('{session}', cur_session)
            data = database.get_items()
            page = fill_page(page, data, STRING_MODE)
            # logging.debug(page)
            print(page)

    else:
        logging.debug('PERMISSION DENIED')

        page = change_html(LOGIN_PAGE, FILE_MODE)
        page = page.replace(FORMAT_PLACE, HTML_WRONG_PASS)
        print(page)

elif 'Sign_up' in form:

    print(change_html(SIGN_UP_PATTERN))
