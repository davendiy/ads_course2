#!/usr/bin/env python3
# -*-encoding: utf-8-*-
""" CGI скрипт обробки натиснення кнопки Buy
"""

import cgi
from sceleton import *
import pickle

form = cgi.FieldStorage()

if 'Buy' in form:

    # перевірка сесії, щоб хто завгодно, без авторизації, не мав доступу до купівлі
    cur_session = form[SESSION_PARAM].value

    with open(SESSIONS_URL, 'rb') as file:  # check session
        sessions = pickle.load(file)  # type: dict
    logging.debug('session id: {}'.format(cur_session))
    user_id = sessions.get(cur_session, None)
    logging.debug('user_id: {}'.format(user_id))
    if user_id is None:
        print(ERROR_PAGE.format('INVALID SESSION'))
        exit(1)

    database.close_cart(user_id)
    print(create_home_page(page_path=HOME_USER_PAGE_PATTERN,
                           cur_session=cur_session,
                           button_template=BUTTON_ADD.replace('{session}', cur_session)))
