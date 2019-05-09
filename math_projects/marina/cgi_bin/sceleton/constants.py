#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# -------------------------- шляхи до шаблонів сторінок ----------------------------------------------
HOME_USER_PAGE_PATTERN = 'front/user_pattern.html'
CART_PAGE_PATTERN = 'front/cart_pattern.html'
ADD_PAGE_PATTERN = 'front/addition_pattern.html'
ADMIN_PAGE_PATTERN = 'front/admin_pattern.html'
PRODUCT_PATTERN = "front/product.html"
SIGN_UP_PATTERN = 'front/sign_up.html'
LOGIN_PAGE = 'front/login.html'

# ----------------------------------------------------------------------------------------------------
STYLESHEET = 'front/main.css'      # шлях до css файлу

SESSIONS_URL = '.tmpfile'      # файл, в якому зберігаються сесії


# шматок html сторінки, яка виводиться при неправильному логіні
HTML_WRONG_PASS = """

<p align=center>
    <font size="4" color="red">

         Incorrect login/password. Try again.
    </font>
</p>
"""

# сторінка, яка виводить помилку
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

# ------------------------- параметри методів POST i GET---------------------------------------------
FORMAT_PLACE = "<!--LIST_HERE-->"   # місце в html сторінці, куди буде вставлятись елемент списку
CREATE_PARAM = 'page_type'          # параметр, який передається, коли необхідно створити сторінку
ADDING_PARAM = 'adding'             # параметр на додавання

# словник 'параметр': 'шлях до необхідної сторінки'
PARAMS_PAGE_DICT = {'admin': ADMIN_PAGE_PATTERN,
                    'cart': CART_PAGE_PATTERN,
                    'addition': ADD_PAGE_PATTERN,
                    'user': HOME_USER_PAGE_PATTERN}

SESSION_PARAM = 'session'   # параметр, що вказує на ідентифікатор сесії
UPDATE_PARAM = 'Update'     # параметр, який передається, коли необхідно оновити сторінку
PARAM_ADD = 'Add2Cart'      # параметр, який передається, коли необхідно додати до корзини
PARAM_DEL = 'Delete'        # параметр, який передається, коли необхідно видалити з корзини


# ------------------------------ параметри, пов'язані з базою даних -----------------------------------

UPLOAD_DIR = 'uploads'      # папка з завантаженнями

DEFAULT_DATABASE = 'storage.db'  # шлях за умовчанням до бази даних

CATEGORIES_TABLE = 'Categories'  # назва таблиці категорій
ITEMS_TABLE = 'Items'            # назва таблиці з товарами
CARTS_TABLE = 'Carts_items'      # назва таблиці з корзиною
USERS_TABLE = 'Users'            # назва таблиці з користувачами

CATEGORIES_FIELDS = ('Id', 'Name')     # поля таблиці категорій

# поля таблиці з товарами
ITEMS_FIELDS = ('Id', 'Name', 'Category_id', 'Description', 'Characteristics', 'Photo', 'Price')

# поля таблиці з корзинами
CARTS_FIELDS = ('Item_id', 'User_id')

# поля таблиці з користувачами
USERS_FIELDS = ('Id', 'Name', 'Password_hash')

# ------------------------------------- інші константи ---------------------------------------------------
FILE_MODE = 'file'       # режими функції change_html
STRING_MODE = 'string'

ADMIN = 'admin'

# шаблон кнопки додавання
BUTTON_ADD = """
<form method="post" action="../cgi_bin/cart.py">
    <input type="submit" name="Add2Cart" value="Add to cart" class='button'>
    <input type="hidden" name="session" value="{session}">
    <input type="hidden" name="Item_id" value="{Item_id}">
    <input type="hidden" name="type" value="Add">
</form>
"""

# шаблон кнопки видалення
BUTTON_DELETE = """
<form method="post" action="../cgi_bin/cart.py">
    <input type="submit" name="Delete" value="Remove from cart" class='button'>
    <input type="hidden" name="session" value="{session}">
    <input type="hidden" name="Item_id" value="{Item_id}">
    <input type="hidden" name="type" value="Delete">
</form>
"""