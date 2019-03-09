#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import sqlite3
import datetime
from .other_functions import *


def default():
    database = BudgetDB(DEFAULT_DATABASE)
    data_connector = BudgetCollection(database)
    return database, data_connector


class BudgetDB:
    """Клас з'єднання з базою даних курсів.

    self.urn - розташування БД курсів
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

    def get_data_dicts(self, query, *parameters, n=DEFAULT_N) -> list:
        """Повертає список словників з даними.

        Як відповідь на запит query з параметрами param.
        :param query: запит SqLite
        :param parameters: змінні параметри запиту, якщо є
        :param n: к-ть елеменів, які повернуться
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        curs = self.get_cursor()
        curs.execute(query, parameters)
        # взято з Mark Lutz - Programming Python.
        # отримати назви полів
        colnames = [desc[0] for desc in curs.description]
        # створити список словників
        rowdicts = [dict(zip(colnames, row)) for row in curs.fetchmany(n)]
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


class BudgetCollection:

    def __init__(self, db: BudgetDB):
        self.db = db
        self.balance = 0
        self.config_file = DEFAULT_CONFIG_FILE
        self.balance = 0
        self.update_balance()

    def update_balance(self):
        self.balance = self.get_sum(item_type=REVENUE) - self.get_sum(item_type=COST)

    def get_items(self, item_type=REVENUE, category='', n=DEFAULT_N) -> list:
        params = ()
        if category:
            if item_type == REVENUE:
                category_id = self.db.get_one_result("SELECT id FROM Categories_in WHERE Name=?", category)
            else:
                category_id = self.db.get_one_result("SELECT id FROM Categories_out WHERE Name=?", category)
            query = "SELECT * from " + item_type + " WHERE Category_id=?"
            params = category_id
        else:
            query = "SELECT * FROM " + item_type

        items = self.db.get_data_dicts(query, *params, n=n)
        return items

    def get_categories(self, item_type=REVENUE):
        """ Отримати список категорій

        :param item_type: REVENUE or COST
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        if item_type == REVENUE:
            item_type = 'Categories_in'
        else:
            item_type = 'Categories_out'

        query = "SELECT * FROM " + item_type
        categories = self.db.get_data_dicts(query)
        return categories

    def add_item(self, Date, Sum, Category_id, Comments='', item_type=REVENUE):

        query = 'INSERT into ' + item_type + '(Date, Sum, Category_id, Comments) values (?, ?, ?, ?)'

        curs = self.db.get_cursor()
        curs.execute(query, (Date, Sum, Category_id, Comments))
        self.db.close()

    def delete_item(self, item_id, item_type=REVENUE):
        curs = self.db.get_cursor()
        curs.execute("DELETE FROM " + item_type + " WHERE id=?",
                     (item_id,))

        self.db.close()

    def change_item(self, id, Date, Sum, Category_id, item_type=REVENUE, Comments=''):
        query = 'UPDATE ' + item_type + " SET date=?, sum=?, category_id=?, comments=? WHERE id=?"
        curs = self.db.get_cursor()
        curs.execute(query, (Date, Sum, Category_id, Comments, id))
        self.db.close()

    def add_category(self, name, item_type):
        if item_type == REVENUE:
            item_type = 'Categories_in'
        else:
            item_type = 'Categories_out'
        query = 'INSERT into ' + item_type + "(Name) values (?)"
        curs = self.db.get_cursor()
        curs.execute(query, (name, ))
        self.db.close()

    def delete_category(self, name, item_type):
        if item_type == REVENUE:
            category_table = 'Categories_in'
        else:
            category_table = 'Categories_out'

        item_id = self.db.get_one_result('SELECT id FROM '+category_table+' WHERE Name=?', name)
        curs = self.db.get_cursor()

        if item_id:
            curs.execute('DELETE FROM '+category_table+' WHERE Name=?', (name,))
            curs.execute('DELETE FROM '+item_type+' WHERE Category_id=?', (item_id[0],))
        self.db.close()

    def get_sum(self, year='', month='', day='', item_type=REVENUE, Category_id=''):
        if day and month and year:
            param = "{}-{}-{}".format(year, month, day)
        elif month and year:
            param = "{}-{}%".format(year, month)
        elif year:
            param = '{}%'.format(year)
        else:
            param = '%'

        query = "SELECT sum FROM " + item_type + " WHERE (Date LIKE ? AND Category_id LIKE ?)"
        curs = self.db.get_cursor()
        curs.execute(query, (param, Category_id))
        items = curs.fetchall()
        res = sum(map(lambda a: a[0], items))
        self.db.close()
        return res
