#!/usr/bin/env python3
# -*-encoding: utf-8-*-

HOME_USER_PAGE_PATTERN = '/front/main_pattern.html'
CART_PAGE_PATTERN = '/front/cart_pattern.html'
ADD_PAGE_PATTERN = '/front/addition_pattern.html'
ADMIN_PAGE_PATTERN = '/front/admin_pattern.html'

STYLESHEET = '/front/main.css'
LOGIN_PAGE = '/front/login.html'
HOME_USER_PAGE = '/front/main.html'
CART_PAGE = '/front/cart.html'
ADD_PAGE = '/front/addition.html'
ADMIN_PAGE = '/front/admin.html'

SESSIONS_URL = '.tmpfile'

PRODUCT_PATTERN = "/front/product.html"


HTML_WRONG_PASS = """

<p align=center>
    <font size="4" color="red">

         Неверный логин/пароль. Попробуйте снова.
    </font>
</p>
"""

FORMAT_PLACE = "<!--LIST_HERE-->"

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
