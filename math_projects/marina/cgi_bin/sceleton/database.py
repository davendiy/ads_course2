#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
Схема бази даних:

    Categories  -> Id
                -> Name

    Items       -> Id
                -> Name
                -> Category_id  >---- Id (from Categories)
                -> Description
                -> Characteristics
                -> Photo

    Users       -> Id
                -> Name
                -> Password_hash

    Carts_items -> Item_id   >-----  Id (from Items)
                -> User_id   >-----  Id (from Users)
"""

from .constants import *
import sqlite3


class Connector:
    """Клас з'єднання з базою даних.

    self.urn - розташування БД
    self.conn - об'єкт зв'язку з базою даних
    """

    def __init__(self, urn):
        self.urn = urn
        self.conn = None

    def get_cursor(self):
        """Повертає об'єкт курсор."""
        self.conn = sqlite3.connect(self.urn)  # зв'язатись з БД
        return self.conn.cursor()

    def close(self):
        """Завершує з'єднання з БД."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
        self.conn = None

    def get_fields(self, tablename: str):
        """ Отримати назви полів з таблиці

        :param tablename: назва таблиці
        :return: ['field1', 'field2', ...]
        """
        curs = self.get_cursor()
        curs.execute("SELECT * from {}".format(tablename))
        res = [desc[0] for desc in curs.description]
        self.close()
        return res

    def get_data_dicts(self, query, *parameters) -> list:
        """Повертає список словників з даними.

        Як відповідь на запит query з параметрами param.
        :param query: запит SqLite
        :param parameters: змінні параметри запиту, якщо є
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        curs = self.get_cursor()
        curs.execute(query, parameters)
        # взято з Mark Lutz - Programming Python.
        # отримати назви полів
        colnames = [desc[0] for desc in curs.description]
        # створити список словників
        rowdicts = [dict(zip(colnames, row)) for row in curs.fetchall()]
        self.close()
        return rowdicts

    def get_one_result(self, query, *parameters):
        """ Повернути однин результат запиту

        :param query: запит SqLite
        :param parameters: змінні параметри запиту, якщо є
        :return: те саме, що і curs.fetchone()
        """
        curs = self.get_cursor()
        curs.execute(query, parameters)
        result = curs.fetchone()
        self.close()
        return result


class ShopStorage:

    def __init__(self, db: Connector):
        self.db = db

    def get_items(self, category=''):
        if category:
            category_id = self.get_category_id(category)
            query = 'SELECT * FROM {} WHERE Category_id=?'.format(CATEGORIES_TABLE)
            res = self.db.get_data_dicts(query, category_id)
        else:
            query = 'SELECT * FROM {}'.format(CATEGORIES_TABLE)
            res = self.db.get_data_dicts(query)
        return res

    def get_category_id(self, category_name):
        query = 'SELECT Id FROM {} WHERE Name=?'.format(CATEGORIES_TABLE)
        res = self.db.get_one_result(query, category_name)
        return '' if not res else res[0]

    def get_categories(self):
        return self.db.get_data_dicts('SELECT * FROM {}'.format(CATEGORIES_TABLE))

    def add_record(self, item_type, **params):

        assert item_type in [CATEGORIES_TABLE, USERS_TABLE, ITEMS_TABLE, CARTS_TABLE]

        # словник -> список кортежів для того, щоб не змінювався порядок елементів
        tmp_params = list(params.items())

        # формуємо запит виду INSERT INTO table (param1, param2) values (?, ?)
        query = 'INSERT INTO {}'.format(item_type) \
                + '(' + ', '.join([el[0] for el in tmp_params]) + ')' \
                + ' values (' + ('?, ' * len(tmp_params)).strip(', ') + ")"
        parameters = [el[1] for el in tmp_params]  # значення параметрів
        # print(query)
        curs = self.db.get_cursor()
        curs.execute(query, parameters)
        self.db.close()

    def get_cart(self, user_id):

        query = 'SELECT Item_id FROM {} WHERE User_id=?'.format(CARTS_TABLE)
        return self.db.get_data_dicts(query, user_id)

    def close_cart(self, user_id):
        query = 'DELETE FROM {} WHERE User_id=?'.format(user_id)
        curs = self.db.get_cursor()
        curs.execute(query)
        self.db.close()


default_conn = Connector(DEFAULT_DATABASE)
database = ShopStorage(default_conn)
