#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 24.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class DequeException(Exception):
    pass


class Node:
    """ Допоміжний клас - вузол деку """

    def __init__(self, item):
        """ Конструктор вузла деку

        :param item: Елемент деку
        """
        self.item = item  # поле, що містить елемент деку
        self.next = None  # наступний вузол
        self.prev = None  # попередній вузол


class Deque:
    """ Реалізує дек як рекурсивну структуру. """

    def __init__(self):
        """ Конструктор деку - Створює порожній дек.
        """
        self.front = None  # Посилання на перший елемент деку
        self.back = None   # Посилання на останній елемент деку
        self._size = 0

    def empty(self):
        """ Перевіряє чи дек порожній

        :return: True, якщо дек порожній
        """
        return self.front is None and self.back is None

    def appendleft(self, item):
        """ Додає елемент до початку деку

        :param item: елемент, що додається
        :return: None
        """
        node = Node(item)           # створюємо новий вузол деку
        node.next = self.front      # наступний вузол для нового - це елемент, який є першим
        if not self.empty():        # якщо додаємо до непорожнього деку
            self.front.prev = node  # новий вузол стає попереднім для першого
        else:
            self.back = node  # якщо додаємо до порожнього деку, новий вузол буде й останнім
        self.front = node     # новий вузол стає першим у деку
        self._size += 1
        print('ok')

    def popleft(self):
        """ Повертає елемент з початку деку.

        :return: Перший елемент у деку
        """
        if self.empty():
            raise DequeException('pop_front: Дек порожній')
        node = self.front       # node - перший вузол деку
        item = node.item        # запам'ятовуємо навантаження
        self.front = node.next  # першим стає наступний вузлом деку
        if self.front is None:  # якщо в деку був 1 елемент
            self.back = None    # дек стає порожнім
        else:
            self.front.prev = None  # інакше перший елемент посилається на None
        del node                    # Видаляємо вузол
        self._size -= 1
        return item

    # методи append та pop повністю симетричні appendleft та popleft відповідно
    def append(self, item):
        """ Додає елемент у кінець деку

        :param item: елемент, що додається
        :return: None
        """
        elem = Node(item)
        elem.prev = self.back
        if not self.empty():
            self.back.next = elem
        else:
            self.front = elem
        self.back = elem
        self._size += 1
        print('ok')

    def pop(self):
        """ Повертає елемент з кінця деку.

        :return: Останній елемент у деку
        """
        if self.empty():
            raise DequeException('pop_back: Дек порожній')
        node = self.back
        item = node.item
        self.back = node.prev
        if self.back is None:
            self.front = None
        else:
            self.back.next = None
        del node
        self._size -= 1
        return item

    def get_front(self):
        if self.empty():
            raise DequeException('get_front: Дек порожній')
        return self.front.item

    def get_back(self):
        if self.empty():
            raise DequeException("get_back: Дек порожній")
        return self.back.item

    def __del__(self):
        """ Деструктор - використовується для коректного видалення
            усіх елементів деку у разі видалення самого деку

        :return: None
        """
        while self.front is not None:  # проходимо по всіх елементах деку
            node = self.front  # запам'ятовуємо посилання на елемент
            self.front = self.front.next  # переходимо до наступного елементу
            del node  # видаляємо елемент
        self.back = None

    def size(self):
        return self._size
