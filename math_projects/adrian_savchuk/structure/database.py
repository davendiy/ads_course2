#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Модуль з класами для зв'язку з базою даних.


Схема бази даних:

    Categories_in  -> id
                   -> Name

    Categories_out -> id
                   -> Name

    Revenues -> id
             -> Date
             -> Sum
             -> Category_id >---- Categories_in.id
             -> Comments

    Costs -> id
          -> Date
          -> Sum
          -> Category_id >---- Categories_out.id
          -> Comments

"""


import sqlite3
from .other_functions import *
import datetime


class BudgetDB:
    """Клас з'єднання з базою даних бюджету.

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
    """ Клас, що забезпечує функціонал домашнього бюджету.
    """

    def __init__(self, db: BudgetDB):
        self.db = db
        self.balance = 0   # різниця між доходами і витратами - нинішня сума
        self.update_balance()

    def update_balance(self):
        """ Порахувати баланс
        """
        self.balance = self.get_sum(item_type=REVENUE) - self.get_sum(item_type=COST)

    def get_items(self, item_type=REVENUE, category='', n=DEFAULT_N) -> list:
        """ Отримати транзакції з бази даних з певними ознаками

        :param item_type: REVENUE або COST
        :param category: назва категорії (опціонально)
        :param n: к-ть транзакцій, що повернуться
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        params = ()
        # формуємо запит відповідно до введених параметрів
        if category:     # якщо вказано категорію, то необхідно знайти її id у БД
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
        """ Додати транзакцію (дохід або витрата). Назви вхідних параметрів
        збігаються з назвами полів  в БД для виключення плутанини.

        :param Date: дата транзакції
        :param Sum: сума
        :param Category_id: номер категорії (з Categories_in/Categories_out)
        :param Comments: коментар (опціонально)
        :param item_type: REVENUE or COST
        """
        query = 'INSERT into ' + item_type + '(Date, Sum, Category_id, Comments) values (?, ?, ?, ?)'

        curs = self.db.get_cursor()
        curs.execute(query, (Date, Sum, Category_id, Comments))
        self.db.close()

    def delete_item(self, item_id, item_type=REVENUE):
        """ Видалити тразнакцію з БД.

        :param item_id: id елемента
        :param item_type: REVENUE or COST
        """
        curs = self.db.get_cursor()
        curs.execute("DELETE FROM " + item_type + " WHERE id=?",
                     (item_id,))

        self.db.close()

    def change_item(self, id, Date, Sum, Category_id, item_type=REVENUE, Comments=''):
        """ Змінити параметри транзакції.

        :param id: ідентифікаційний номер (адреса транзакції, не міняється)
        :param Date: дата
        :param Sum: сума
        :param Category_id: номер категорії (3 Categories_in/Categories_out)
        :param item_type: REVENUE or COST
        :param Comments: коментар (опціонально)
        """

        query = 'UPDATE ' + item_type + " SET date=?, sum=?, category_id=?, comments=? WHERE id=?"
        curs = self.db.get_cursor()
        curs.execute(query, (Date, Sum, Category_id, Comments, id))
        self.db.close()

    def add_category(self, name, item_type):
        """ Додати нову категорію у відповідну таблицю.

        :param name: назва
        :param item_type: REVENUE or COST
        """
        if item_type == REVENUE:
            item_type = 'Categories_in'
        else:
            item_type = 'Categories_out'
        query = 'INSERT into ' + item_type + "(Name) values (?)"
        curs = self.db.get_cursor()
        curs.execute(query, (name, ))
        self.db.close()

    def delete_category(self, name, item_type):
        """ Видалити категорію і всі транзакції цієї категорії.

        :param name: назва категорії
        :param item_type: REVENUE or COST
        """
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

    def get_sum(self, year='', month='', day='', item_type=REVENUE, Category_id='%'):
        """ Порахувати суму всіх транзакцій певного типу за певний період.

        :param year: рік, у який відбувалась транзакція (опціонально)
        :param month: місяць, у який відбувалась транзакція (опціонально)
        :param day: день, у який відбувалась транзакція (опціонально)
        :param item_type: REVENUE or COST
        :param Category_id: номер категорії
        :return: int/float
        """
        # формуємо параметр парсингу по даті
        if day and month and year:
            param = "{}-{}-{}".format(year, month, day)
        elif month and year:
            param = "{}-{}%".format(year, month)
        elif year:
            param = '{}%'.format(year)
        else:
            param = '%'

        # формуємо запит відповідно до заданих дати і категорії
        query = "SELECT sum FROM " + item_type + " WHERE (Date LIKE ? AND Category_id LIKE ?)"
        curs = self.db.get_cursor()
        curs.execute(query, (param, Category_id))
        items = curs.fetchall()
        res = sum(map(lambda a: a[0], items))
        self.db.close()
        return res
