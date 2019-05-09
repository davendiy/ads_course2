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
                -> Price

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
        """ Повернути товари певної категорії

        :param category: назва категорії
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        if category:
            category_id = self.get_category_id(category)
            if category_id:
                query = 'SELECT * FROM {} WHERE Category_id=?'.format(ITEMS_TABLE)
                res = self.db.get_data_dicts(query, category_id)
            else:
                res = []
        else:
            query = 'SELECT * FROM {}'.format(ITEMS_TABLE)
            res = self.db.get_data_dicts(query)

        return res
        
    def get_category_id(self, category_name):
        """ Повернути ідентифікаций номер категорії за її назвою

        :param category_name: назва категорії
        :return: ід
        """
        query = 'SELECT Id FROM {} WHERE Name=?'.format(CATEGORIES_TABLE)
        res = self.db.get_one_result(query, category_name)
        return '' if not res else res[0]

    def get_categories(self):
        """ Повернути список всіх категорій

        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        return self.db.get_data_dicts('SELECT * FROM {}'.format(CATEGORIES_TABLE))

    def add_record(self, item_type, **params):
        """ Додати запис до бази даних

        :param item_type: [CATEGORIES_TABLE, USERS_TABLE, ITEMS_TABLE, CARTS_TABLE] - тип запису (назва таблиці)
        :param params: параметри запису
        """
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

    def del_record(self, item_type, item_id):
        """ Видалити запис з бази даних

        :param item_type: [CATEGORIES_TABLE, USERS_TABLE, ITEMS_TABLE, CARTS_TABLE] - тип запису (назва таблиці)
        :param item_id: id елемента
        """
        assert item_type in [CATEGORIES_TABLE, USERS_TABLE, ITEMS_TABLE, CARTS_TABLE]

        if item_type == CARTS_TABLE:
            query = "DELETE FROM {} WHERE Item_id=?".format(item_type)
        else:
            query = "DELETE FROM {} WHERE Id=?".format(item_type)

        curs = self.db.get_cursor()
        curs.execute(query, (item_id,))
        self.db.close()

    def get_cart(self, user_id):
        """ Отримати елементи, що знаходяться в корзині користувача з заданим id

        :param user_id: число
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        query = 'SELECT Item_id FROM {} WHERE User_id=?'.format(CARTS_TABLE)
        return self.db.get_data_dicts(query, user_id)

    def close_cart(self, user_id):
        """ Здійснити купівлю

        Видаляє з корзини користувача всі елементи + видаляє ці елементи з загальної таблиці
        :param user_id: число (ідентифікатор користувача)
        """
        items = self.get_cart(user_id)
        for el in items:
            self.del_record(ITEMS_TABLE, item_id=el['Item_id'])
        query = 'DELETE FROM {} WHERE User_id=?'.format(CARTS_TABLE)
        curs = self.db.get_cursor()
        curs.execute(query, (user_id,))
        self.db.close()

    def get_user_pass(self, user):
        """ Повернути хеш пароля користувача

        :param user: логін користувача
        :return: хеш пароля
        """
        query = 'SELECT Password_hash FROM {} WHERE Name=?'.format(USERS_TABLE)
        res = self.db.get_one_result(query, user)
        return '' if not res else res[0]

    def get_user_id(self, user):
        """ Повернути ід користувача за іменем

        :param user: ім'я (логін)
        :return: ід (число)
        """
        query = 'SELECT Id FROM {} WHERE Name=?'.format(USERS_TABLE)
        res = self.db.get_one_result(query, user)
        return '' if not res else res[0]

    def get_one_item(self, item_id):
        """ Повернути 1 елемет з таблиці за даним ід

        :param item_id: ідентифікатор елемента
        :return: {name_field1: value1, name_field2: value2 ...}
        """
        query = 'SELECT * FROM {} WHERE Id=?'.format(ITEMS_TABLE)
        res = self.db.get_data_dicts(query, item_id)
        return '' if not res else res[0]


# об'єкти за замовчуванням
default_conn = Connector(DEFAULT_DATABASE)
database = ShopStorage(default_conn)
