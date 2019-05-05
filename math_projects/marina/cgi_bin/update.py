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
    user_id = sessions.get(cur_session, None)
    if user_id is None:
        print(ERROR_PAGE)
        exit(1)

    page_type = form[CREATE_PARAM].value
    page_path = PARAMS_PAGE_DICT[page_type]
    page = change_html(page_path)
    page = page.replace('{session}', cur_session)
    category = form['Category'].value if 'Category' in form else ''
    page = fill_page(page, database.get_items(category), STRING_MODE)
    print(page)
