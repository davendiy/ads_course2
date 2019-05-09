#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" CGI скрипт створення необхідної html сторінки, після натиснення
відповідної кнопки на попередній сторінці
"""

import cgi
from sceleton import *
import pickle
import cgitb

cgitb.enable()
form = cgi.FieldStorage()

if CREATE_PARAM in form:
    page_type = form[CREATE_PARAM].value    # зчитка полів форми
    page_path = PARAMS_PAGE_DICT[page_type]
    cur_session = form[SESSION_PARAM].value

    with open(SESSIONS_URL, 'rb') as file:    # check session
        sessions = pickle.load(file)   # type: dict
    logging.debug('session id: {}'.format(cur_session))
    user_id = sessions.get(cur_session, None)
    logging.debug('user_id: {}'.format(user_id))
    if user_id is None:
        print(ERROR_PAGE.format('INVALID SESSION'))
        exit(1)

    # створення відповідної сторінки
    if page_path == ADMIN_PAGE_PATTERN:
        print(create_home_page(page_path, cur_session, ''))

    elif page_path == HOME_USER_PAGE_PATTERN:
        print(create_home_page(page_path, cur_session, BUTTON_ADD.replace('{session}', cur_session)))

    elif page_path == CART_PAGE_PATTERN:
        print(create_cart_page(page_path, cur_session, BUTTON_DELETE.replace('{session}', cur_session), user_id))

    elif page_path == ADD_PAGE_PATTERN:
        page = change_html(page_path, FILE_MODE)
        page = page.replace('{session}', cur_session)
        print(page)

    else:
        logging.debug('INVALID PAGE_PATH')
        print(ERROR_PAGE)
        exit(1)
