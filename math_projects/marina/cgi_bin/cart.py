#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import cgi
from sceleton import *
import pickle

form = cgi.FieldStorage()

if PARAM_ADD in form or PARAM_DEL in form:

    item_id = form['Item_id'].value
    cur_session = form['session'].value

    with open(SESSIONS_URL, 'rb') as file:    # check session
        sessions = pickle.load(file)   # type: dict
    logging.debug('session id: {}'.format(cur_session))
    user_id = sessions.get(cur_session, None)
    logging.debug('user_id: {}'.format(user_id))
    logging.debug('sessions: {}'.format(sessions))
    if user_id is None:
        print(ERROR_PAGE.format('INVALID SESSION'))
        exit(1)

    if PARAM_ADD in form:
        database.add_record(item_type=CARTS_TABLE, Item_id=item_id, User_id=user_id)
        page = change_html(HOME_USER_PAGE_PATTERN, FILE_MODE)
        page = page.replace('{session}', cur_session)
        data = database.get_items()
        logging.debug('data for cart page: {}'.format(data))
        page = fill_page(page, data, mode=STRING_MODE, button_template=BUTTON_ADD.replace('{session}', cur_session))
        print(page)
    else:
        database.del_record(item_type=CARTS_TABLE, item_id=item_id)

        page = change_html(CART_PAGE_PATTERN, FILE_MODE)
        page = page.replace('{session}', cur_session)
        tmp_data = database.get_cart(user_id)
        data = []
        for el in tmp_data:
            data.append(database.get_one_item(el['Item_id']))
        logging.debug('data for cart page: {}'.format(data))
        page = fill_page(page, data, mode=STRING_MODE, button_template=BUTTON_DELETE.replace('{session}', cur_session))
        print(page)
