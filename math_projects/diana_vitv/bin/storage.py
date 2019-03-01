#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 10.02.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import sqlite3


class StorageDB:
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

    def get_data_dicts(self, query, *parameters, n=20):
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


class StorageCollection:
    """Клас для отримання даних курсів.

    self.db - об'єкт БД
    """

    def __init__(self, db):
        self.db = db     # type: StorageDB

    def get_items(self, category='', n=20):
        """ Повертає всі товари на складі (певної категорії, якщо вказано).

        :param category: рядок
        :param n: к-ть елементів, які поверне пошук
        :return: словник {назва поля: елементи}
        """
        params = ()
        if category:
            category_id = self.db.get_one_result("SELECT id FROM categories WHERE Name=?", category)
            query = "SELECT * from items WHERE Category_id=?"
            params = (category_id, )
        else:
            query = "SELECT * FROM items"

        items = self.db.get_data_dicts(query, *params, n=n)
        return items

    def get_categories(self):
        """ Отримати список категорій

        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        query = "SELECT * FROM categories"
        categories = self.db.get_data_dicts(query)
        return categories

    def find_item(self, piece_of_name: str, category='', n=20):
        """ Знайти товар за частиною імені та категорією

        :param piece_of_name: рядок
        :param n: к-ть елементів, які повернуться
        :param category: категорія, якщо є
        :return: [{name_field1: value1, name_field2: value2 ...}, ...]
        """
        piece_of_name = '%' + piece_of_name + '%'
        if category:
            query = "SELECT * from items WHERE (Name LIKE ? AND Category_id=?)"
            items = self.db.get_data_dicts(query, piece_of_name.lower(), category, n=n)
        else:
            query = "SELECT * from items WHERE (Name LIKE ?)"
            items = self.db.get_data_dicts(query, piece_of_name.lower(), n=n)
        return items

    def add_item(self, name, category_id, department_id, build_number, shelf_number):
        """ Додає товар до складу

        :param name: назва (будь-яка)
        :param category_id: ід катеогорії (необхідно взяти з categories за назвою)
        :param department_id: будь-який ід
        :param build_number: будь-який ід
        :param shelf_number: будь-який ід
        """
        query = 'INSERT into items(Name, Category_id, Department_id, Build_number, Shelf_number) ' \
                'values (?, ?, ?, ?, ?)'

        curs = self.db.get_cursor()               # FIXME it seems to be false
        curs.execute(query, (name, category_id, department_id, build_number, shelf_number))
        self.db.close()

    def change_item(self, item_id, name, category_id, department_id, build_number, shelf_number):
        """ Змінює товар на складі

        :param item_id: ід
        :param name: нове ім'я
        :param category_id: новий ід категорії (з categories)
        :param department_id: новий ід відділу
        :param build_number: новий номер будинку
        :param shelf_number: новий номер полиці
        :return:
        """
        query = "UPDATE items SET Name=?, Category_id=?, Department_id=?, Build_number=?, Shelf_number=?" \
                "WHERE id=?"

        curs = self.db.get_cursor()
        curs.execute(query, [name, category_id, department_id, build_number, shelf_number, item_id])
        self.db.close()

    def delete_item(self, item_id):
        """ Видаляє товар за ід
        :param item_id: ід елемента в базі даних
        """
        curs = self.db.get_cursor()
        curs.execute("DELETE FROM items WHERE id=?",
                     (item_id,))
        self.db.close()

    def add_category(self, name):
        """ Додати категорію

        :param name: назва
        """
        curs = self.db.get_cursor()
        curs.execute('INSERT into categories(Name) values (?)', (name,))
        self.db.close()

    def delete_category(self, name):
        """ Видалити категорію і всі товари такої категорії

        :param name: назва
        """
        item_id = self.db.get_one_result('SELECT id FROM categories WHERE Name=?', name)
        curs = self.db.get_cursor()
        curs.execute('DELETE FROM categories WHERE Name=?', (name,))
        curs.execute('DELETE FROM items WHERE Category_id=?', (item_id,))
        self.db.close()


if __name__ == '__main__':

    test = StorageCollection('source.db')
    while True:
        try:
            eval(input('--> '))
        except Exception as e:
            print(e)
