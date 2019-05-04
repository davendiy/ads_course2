#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from .sceleton import *
import pickle

form = cgi.FieldStorage()

if ADDING_PARAM in form:
    cur_session = form[SESSION_PARAM]

    with open(SESSIONS_URL, 'rb') as file:  # check session
        sessions = pickle.load(file)  # type: dict
    user_id = sessions.get(cur_session, None)
    if user_id is None:
        print(ERROR_PAGE)
        exit(1)

    params = {el: form[el].value if el in form else '' for el in ITEMS_FIELDS if el != 'Id'}
    try:
        database.add_record(ITEMS_TABLE, **params)
        page = change_html(ADD_PAGE_PATTERN, FILE_MODE)
        page = page.format(session=cur_session)
        print(page)
    except Exception as e:
        print(e)
