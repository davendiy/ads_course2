#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from .sceleton import *
import pickle

form = cgi.FieldStorage()

if CREATE_PARAM in form:
    page_type = form[CREATE_PARAM].value
    page_path = PARAMS_PAGE_DICT[page_type]
    cur_session = form[SESSION_PARAM]

    with open(SESSIONS_URL, 'rb') as file:    # check session
        sessions = pickle.load(file)   # type: dict
    user_id = sessions.get(cur_session, None)
    if user_id is None:
        print(ERROR_PAGE)
        exit(1)

    if page_path in [ADMIN_PAGE_PATTERN, HOME_USER_PAGE_PATTERN]:
        page = change_html(page_path, FILE_MODE)
        page = page.format(session=cur_session)
        data = database.get_items()
        page = fill_page(page, data, mode=STRING_MODE)
        print(page)

    elif page_path == CART_PAGE_PATTERN:
        page = change_html(page_path, FILE_MODE)
        page = page.format(session=cur_session)
        data = database.get_cart(user_id)
        page = fill_page(page, data, mode=STRING_MODE)
        print(page)

    elif page_path == ADD_PAGE_PATTERN:
        page = change_html(page_path, FILE_MODE)
        page = page.format(session=cur_session)
        print(page)

    else:
        print(ERROR_PAGE)
        exit(1)
