#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from sceleton import *
import pickle

form = cgi.FieldStorage()

if UPDATE_PARAM in form:
    cur_session = form[SESSION_PARAM].value

    with open(SESSIONS_URL, 'rb') as file:  # check session
        sessions = pickle.load(file)  # type: dict
    logging.debug('sessions: {}'.format(sessions))
    user_id = sessions.get(cur_session, None)
    if user_id is None:
        print(ERROR_PAGE)
        exit(1)

    page_type = form[CREATE_PARAM].value
    page_path = PARAMS_PAGE_DICT[page_type]
    category = form['Category'].value if 'Category' in form else ''
    tmp = BUTTON_ADD.replace('{session}', cur_session) if page_type == 'user' else ''
    print(create_home_page(page_path=page_path,
                           cur_session=cur_session,
                           button_template=tmp,
                           category=category))
