#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from .heap import Heap


class PQElement:
    """ Клас Елемент пріорітетної черги """

    INF = 100000                   # Умовна нескінченність

    def __init__(self, item=None, priority=INF):
        """ Конструктор

        :param item: Ключ (ім'я) елементу
        :param priority: Пріорітет
        """
        self.mItem = item
        self.mPriority = priority

    def setPriority(self, priority):
        """ Встановлює пріоритет для поточного елементу

        :param priority: Пріорітет
        :return: None
        """
        self.mPriority = priority

    def setItem(self, item):
        """ Встановлення ключа поточного елементу

        :param item: Нове значення ключа
        :return: None
        """
        self.mItem = item

    def priority(self):
        """ Повертає поточний пріорітет елементу

        :return: Поточне пріорітет елементу
        """
        return self.mPriority

    def item(self):
        """ Повертає ключ елемента

        :return: Ключ елемента
        """
        return self.mItem

    def __getitem__(self, item):
        """ Перевизначає оператор '[]' для читання

        :param item: 0 - для того, щоб взяти ключ елемента, 1 - його пріорітет
        :return: Ключ/пріоритет
        """
        if item == 0:
            return self.mItem
        elif item == 1:
            return self.mPriority
        else:
            raise IndexError

    def __setitem__(self, key, value):
        """ Перевизначає оператор '[]' для запису

        :param key: 0 - для того, щоб взяти ключ елемента, 1 - його пріорітет
        :param value: Ключ/пріоритет
        :return: None
        """
        if key == 0:
            self.mItem = value
        elif key == 1:
            self.mPriority = value
        else:
            raise IndexError

    def __str__(self):
        """ Перевизначає оператор "str()" для черги

        :return: None
        """
        return "(item: {}, priority: {})".format(self.mItem, self.mPriority)

    def __le__(self, other):
        """ Перевизначає оператор '<='

        :param other: інший елемент
        :return: True, якщо пріоритет поточного елементу менший або рівний за пріоритет іншого
        """
        return self.mPriority <= other.mPriority

    def __lt__(self, other):
        """ Перевизначає оператор '<'

        :param other: інший елемент
        :return: True, якщо пріоритет поточного елементу менший за пріоритет іншого
        """
        return self.mPriority < other.mPriority

    def __gt__(self, other):
        """ Перевизначає оператор '>'

        :param other: інший елемент
        :return: True, якщо пріоритет поточного елементу більший за пріоритет іншого
        """
        return self.mPriority > other.mPriority

    def __ge__(self, other):
        """ Перевизначає оператор '>='

        :param other: інший елемент
        :return: True, якщо пріоритет поточного елементу більший або рівний за пріоритет іншого
        """
        return self.mPriority >= other.mPriority


class PriorityQueue(Heap):
    """ Клас пріоритетна черга на базі структури даних Купа """

    def __init__(self):
        """ Конструктор """
        super().__init__()
        self.mElementsMap = {}  # Карта індексів (у масиві, що моделює чергу) елеменітів черги.
        # Є словник з елементів (елемент, індекс)
        # Використовується для визначення чи міститься елемент у черзі
        # а також для швидкої зміни пріорітеру елемента у черзі

    def swap(self, i, j):
        """ Перевизначення методу батьківського класу обміну місцями елементів
            на позиціях i та j у черзі із простеженням позиції елемента у черзі.

        :param i: перший індекс
        :param j: другий індекс
        :return: None
        """
        pos_i = self.mItems[i].item()  # Поточна позиція елемента i у масиві
        pos_j = self.mItems[j].item()  # Поточна позиція елемента j у масиві
        self.mElementsMap[pos_i] = j
        self.mElementsMap[pos_j] = i

        super().swap(i, j)

    def __contains__(self, item):
        """ Перевизначає оператор 'in'

        :param item: Ключ
        :return: True, якщо ключ міститься у черзі
        """
        return item in self.mElementsMap

    def insert(self, *k):
        """ Перевизначення методу батьківського класу Heap для випадку вставки пари: k = (елемент, пріоритет)

        :param k: Кортеж (елемент, пріоритет)
        :return: None
        """

        assert len(k) == 2

        el = PQElement(k[0], k[1])

        self.mSize += 1
        self.mItems.append(el)  # Вставляємо на останню позицію,
        self.mElementsMap[k[0]] = self.mSize  # S

        self.siftUp()  # просіюємо елемент вгору

    def decreasePriority(self, item, priority):
        """ Метод перерахунку пріоритету елемента.

        Працює лише у випадку підвищення пріоритету у черзі, тобто якщо
        значення параметру priority є меншим ніж поточне значення пріоритету
        Працює по принципу, замінюємо пріоритет елемента у черзі та здійснюємо просіювання вгору.

        :param item: Ключ
        :param priority: Новий пріоритет
        :return: True
        """

        i = self.mElementsMap[item]
        self.mItems[i].setPriority(priority)

        # просіювання вгору для елемента зі зміненим пріоритетом
        while i > 1:
            parent = i // 2
            if self.mItems[i] < self.mItems[parent]:
                self.swap(parent, i)
            i = parent

        return True

    def extractMinimum(self):
        """ Повертає елемент черги з мінімальним пріоритетом
            Перевизначає метод батькывського класу Heap для випадку пари - (елемент, пріоритет)

        :return: Елемент черги з мінімальним пріоритетом
        """

        min_el = self.mItems[1][0]  # Запам'ятовуємо значення кореня дерева

        self.mItems[1] = self.mItems[-1]  # Переставляємо на першу позицію останній елемент (за номером) у купі

        pos_last = self.mItems[-1].item()  # Поточна позиція останнього елемента у масиві
        self.mElementsMap[pos_last] = 1  # Переставляємо на першу позицію

        self.mItems.pop()  # Видаляємо останній (за позицією у масиві) елемент купи
        if min_el in self:  # Якщо елемент міститься у черзі
            del self.mElementsMap[min_el]  # Видаляємо елемент з мапи елементів

        self.mSize -= 1

        self.siftDown()  # Здійснюємо операцію просіювання вниз, для того,
        # щоб опустити переставлений елемент на відповідну позицію у купі

        return min_el

    def __str__(self):
        """ Перевизначає оператор "str()"

         :return: Зображення черги у вигляді рядка
         """
        res = ""
        for i in range(1, self.mSize + 1):
            res += str(self.mItems[i]) + "\n"
        return res


if __name__ == "__main__":
    h = PriorityQueue()

    # h.insert(17, 11)
    # h.insert(14, 10)
    # h.insert(33, 9)
    # h.insert(21, 8)
    # h.insert(27, 7)
    h.insert(11, 6)
    h.insert(19, 5)
    h.insert(18, 4)
    h.insert(9, 3)
    h.insert(5, 2)
    h.insert(3, 9)

    print(h)

    h.decreasePriority(11, 1)

    print()
    #
    print(h.extractMinimum())

    # print("==========")

    h.decreasePriority(11, 5)
    # print(h)

    while not h.empty():
        print(h.extractMinimum())
