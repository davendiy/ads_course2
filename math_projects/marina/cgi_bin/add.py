#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" CGI скрипт додавання адміном нового товару
"""

import cgi
from sceleton import *
import pickle
import os
import cgitb

cgitb.enable()    # для дебагу
form = cgi.FieldStorage()


if ADDING_PARAM in form:
    cur_session = form[SESSION_PARAM].value

    # перевірка коректності сесії (щоб не можна було просто так, без авторизації, здійснити додавання)
    with open(SESSIONS_URL, 'rb') as file:
        sessions = pickle.load(file)  # type: dict
    logging.debug('session id: {}'.format(cur_session))
    user_id = sessions.get(cur_session, None)
    logging.debug('user_id: {}'.format(user_id))

    if user_id is None:
        print(ERROR_PAGE)
        exit(1)

    try:
        # намагаємось зчитати всі записи з форми
        params = {el: form[el].value if el in form and el != 'Photo' else '' for el in ITEMS_FIELDS if el != 'Id'}

        # Якщо додана фотографія, як файл.
        if "Photo" in form:
            form_file = form['Photo']
            # form_file is now a file object in python
            if form_file.filename:
                # створюємо файл в загрузках
                uploaded_file_path = os.path.join(UPLOAD_DIR, os.path.basename(form_file.filename))
                with open(uploaded_file_path, 'wb') as fout:
                    # зчитуємо надсилаємий файл по шматках і записуємо його до створеного
                    while True:
                        chunk = form_file.file.read(100000)
                        if not chunk:
                            break
                        # write the file content on a file on the hdd
                        fout.write(chunk)
                params["Photo"] = uploaded_file_path   # запам'ятовуємо шлях до створеного файлу

        # зчитування, додавання до бд, створення сторінки
        logging.debug('params before substitution: {}'.format(params))
        category = form['Category'].value
        category_id = database.get_category_id(category)
        if not category_id:
            database.add_record(item_type=CATEGORIES_TABLE, Name=category)
            category_id = database.get_category_id(category)
        params['Category_id'] = category_id

        logging.debug('params after substitution: {}'.format(params))
        database.add_record(ITEMS_TABLE, **params)
        page = change_html(ADD_PAGE_PATTERN, FILE_MODE)
        page = page.replace('{session}', str(cur_session))
        print(page)
    except Exception as e:
        logging.exception(e)
        print(e)
