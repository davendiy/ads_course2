#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" CGI скрипт реєстрації
"""
import cgi
from sceleton import *

form = cgi.FieldStorage()

if 'Sign_up' in form:

    try:
        login = form['login'].value if 'login' in form else ''
        password = form['password'].value if 'password' in form else ''
        password2 = form['password2'].value if 'password2' in form else ''

        if not login or not password or password2 != password:
            print(ERROR_PAGE.format('Something wrong'))

        pashash = encrypt(password)
        database.add_record(item_type=USERS_TABLE, Name=login, Password_hash=pashash)
        page = change_html(LOGIN_PAGE, FILE_MODE)
        print(page)
    except Exception as e:
        print(ERROR_PAGE.format(e))
