#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import sqlite3


class DataConnector:
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


class Database:

    def __init__(self, database: DataConnector):
        self.db = database

    def get_description(self, name):

        query = "SELECT Description FROM Base WHERE Name=?"
        return self.db.get_one_result(query, name)

    def add_element(self, name, description):
        query = "INSERT into Base (Name, Descriprtion) values (?, ?)"
        curs = self.db.get_cursor()
        curs.execute(query, (name, description))
        self.db.close()


if __name__ == '__main__':
    test_con = DataConnector('test.db')
    test_data = Database(test_con)
    test_curs = test_con.get_cursor()
    test_curs.execute("CREATE TABLE Base (Name TEXT PRIMARY KEY UNIQUE, Description TEXT)")
    test_con.close()

    print('1 - adding new item, 2 - get description by the name, 0 - exit')
    while True:
        try:
            a = input('--> ')
            if a == '1':
                test_name = input('name: ')
                test_desc = input('description: ')
                test_data.add_element(test_name, test_desc)
            elif a == '2':
                test_name = input('name: ')
                print(test_data.get_description(test_name))
            else:
                break
        except Exception as e:
            print("error:", e)
