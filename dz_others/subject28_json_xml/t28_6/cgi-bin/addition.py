#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t28_21_refbook_xml.py - основа

import xml.etree.ElementTree as et


class XMLBookLibrary:
    """Клас для ведення бібліотеки з використанням XML.

       У файлі XML записи довідника зберігаються у форматі:
       <library>
           <book name="назва" author="автор" year="рік видання" />
          ...
       </library>

       Поля:
       self.filename - ім'я файлу довідника
    """

    def __init__(self, filename):
        self.filename = filename

    def createrb(self):
        """Створює довідник та записує у нього n записів."""
        n = int(input('Кількість записів: '))
        book = et.Element('Library')  # створити кореневий вузол дерева
        for i in range(n):
            element = et.Element('Book')
            element.set('name', input('Назва книги: '))
            element.set('author', input('Автор: '))
            element.set('year', input('Рік видання: '))
            book.append(element)  # додати сина (вузол)
        e = et.ElementTree(book)  # створити документ
        e.write(self.filename)  # зберегти файл

    def apprb(self):
        """Доповнює довідник одним записом."""
        # завантажити та проаналізувати документ
        e = et.parse(self.filename)
        book = e.getroot()
        element = et.Element('name')
        element.set('name', input('Назва книги: '))
        element.set('author', input('Автор: '))
        element.set('year', input('Рік видання: '))
        book.append(element)
        e.write(self.filename)  # зберегти файл

    def search(self, name='', author='', year_from='', year_to=''):
        """ Пошук запису з заданими параметрами

        :param name: назва
        :param author: автор
        :param year_from: нижня межа року видання
        :param year_to: верхня межа року видання
        :return: список записів
        """
        e = et.parse(self.filename)

        results = []
        for element in e.iter('Book'):
            succ = True

            # перевіряємо параметри
            if name and name not in element.get('name'):
                succ = False
            if author and author not in element.get('author'):
                succ = False
            if year_from and int(element.get('year')) < int(year_from):
                succ = False
            if year_to and int(element.get('year')) > int(year_to):
                succ = False

            # якщо все норм - додаємо запис до результуючого списку
            if succ:
                results.append([element.get(_) for _ in  ['name', 'author', 'year']])
        return results


# тестування
if __name__ == '__main__':

    filename = 'refs.xml'  # ім'я файлу бібліотеки

    rb = XMLBookLibrary(filename)

    while True:
        k = int(input('Режим роботи [1 - 5]:'))
        if k == 1:  # створити
            rb.createrb()
        elif k == 2:  # додати запис
            rb.apprb()
        elif k == 3:  # знайти запис
            res = rb.search(input('Назва: '), input('Автор: '), input('Від: '), input('До: '))
            print(res)
        elif k == 5:
            break
