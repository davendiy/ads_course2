#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from sceleton import *
import pickle

form = cgi.FieldStorage()

if 'Buy' in form:

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
    page = change_html(HOME_USER_PAGE_PATTERN, FILE_MODE)
    page = page.replace('{session}', cur_session)
    data = database.get_items()
    logging.debug('data for home page: {}'.format(data))
    page = fill_page(page, data, mode=STRING_MODE, button_template=BUTTON_ADD.replace('{session}', cur_session))
    print(page)
