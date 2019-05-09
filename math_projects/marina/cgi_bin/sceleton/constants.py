#!/usr/bin/env python3
# -*-encoding: utf-8-*-

HOME_USER_PAGE_PATTERN = 'front/user_pattern.html'
CART_PAGE_PATTERN = 'front/cart_pattern.html'
ADD_PAGE_PATTERN = 'front/addition_pattern.html'
ADMIN_PAGE_PATTERN = 'front/admin_pattern.html'
PRODUCT_PATTERN = "front/product.html"
SIGN_UP_PATTERN = 'front/sign_up.html'

STYLESHEET = 'front/main.css'
LOGIN_PAGE = 'front/login.html'

SESSIONS_URL = '.tmpfile'


HTML_WRONG_PASS = """

<p align=center>
    <font size="4" color="red">

         Incorrect login/password. Try again.
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
<h1>{}</h1>
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

UPLOAD_DIR = 'uploads'

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


BUTTON_ADD = """
<form method="post" action="../cgi_bin/cart.py">
    <input type="submit" name="Add2Cart" value="Add to cart" class='button'>
    <input type="hidden" name="session" value="{session}">
    <input type="hidden" name="Item_id" value="{Item_id}">
    <input type="hidden" name="type" value="Add">
</form>
"""

BUTTON_DELETE = """
<form method="post" action="../cgi_bin/cart.py">
    <input type="submit" name="Delete" value="Remove from cart" class='button'>
    <input type="hidden" name="session" value="{session}">
    <input type="hidden" name="Item_id" value="{Item_id}">
    <input type="hidden" name="type" value="Delete">
</form>
"""

PARAM_ADD = 'Add2Cart'
PARAM_DEL = 'Delete'
