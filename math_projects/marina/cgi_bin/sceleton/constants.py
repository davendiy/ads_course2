#!/usr/bin/env python3
# -*-encoding: utf-8-*-


HOME_PAGE = '/front/main.html'
CART_PAGE = '/front/cart.html'
ADD_PAGE = '/front/addition.html'
STYLESHEET = '/front/main.css'


PRODUCT_PATTERN = """<div class="product">
    <ul>
        <li>
            <!--название-->
            {}
        </li>
        <li>
            <!--описание-->
            {}
        </li>
        <li>
            <!--характеристики-->
            {}
        </li>
        <li>
            <!--фото-->
            {}
        </li>
        <li>
            <!--цена-->
            {}
        </li>
        <li>
            <!--количество-->
            {}
        </li>

    </ul>
</div>"""


DEFAULT_DATABASE = 'storage.db'

CATEGORIES_TABLE = 'Categories'
ITEMS_TABLE = 'Items'
CARTS_TABLE = 'Carts_items'
USERS_TABLE = 'Users'

CATEGORIES_FIELDS = ('Id', 'Name')
ITEMS_FIELDS = ('Id', 'Name', 'Category_id', 'Description', 'Characteristics', 'Photo')
CARTS_FIELDS = ('Item_id', 'User_id')
USERS_FIELDS = ('Id', 'Name', 'Password_hash')
