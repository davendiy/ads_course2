#!/usr/bin/env python3
# -*-encoding: utf-8-*-

HOME_USER_PAGE_PATTERN = '/front/user_pattern.html'
CART_PAGE_PATTERN = '/front/cart_pattern.html'
ADD_PAGE_PATTERN = '/front/addition_pattern.html'
ADMIN_PAGE_PATTERN = '/front/admin_pattern.html'
PRODUCT_PATTERN = "/front/product.html"

STYLESHEET = '/front/main.css'
LOGIN_PAGE = '/front/login.html'

SESSIONS_URL = '.tmpfile'


HTML_WRONG_PASS = """

<p align=center>
    <font size="4" color="red">

         Неверный логин/пароль. Попробуйте снова.
    </font>
</p>
"""


ERROR_PAGE = """Content-type: text/html charset=utf-8

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ERROR</title>
</head>
<body>
<h1>INVALID SESSION</h1>
</body>
</html>
"""

FORMAT_PLACE = "<!--LIST_HERE-->"
CREATE_PARAM = 'page_type'
ADDING_PARAM = 'adding'
PARAMS_PAGE_DICT = {'admin': ADMIN_PAGE_PATTERN,
                    'cart': CART_PAGE_PATTERN,
                    'addition': ADD_PAGE_PATTERN,
                    'user': HOME_USER_PAGE_PATTERN}

SESSION_PARAM = 'session'
UPDATE_PARAM = 'Update'

DEFAULT_DATABASE = 'storage.db'

CATEGORIES_TABLE = 'Categories'
ITEMS_TABLE = 'Items'
CARTS_TABLE = 'Carts_items'
USERS_TABLE = 'Users'

CATEGORIES_FIELDS = ('Id', 'Name')
ITEMS_FIELDS = ('Id', 'Name', 'Category_id', 'Description', 'Characteristics', 'Photo', 'Price')
CARTS_FIELDS = ('Item_id', 'User_id')
USERS_FIELDS = ('Id', 'Name', 'Password_hash')

FILE_MODE = 'file'
STRING_MODE = 'string'

ADMIN = 'admin'
