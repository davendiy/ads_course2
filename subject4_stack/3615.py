#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
Компанія Giggle відкриває свій новий офіс у Судиславлі, і ви запрошені на співьесіду.
Ваша задача - розв'язати поставлену задачу.

Вам потрібно створити структуру даних, яка являє собою масив цілих чисел.
Спочатку масив порожній. Вам потрібно підтримувати дві операції:

запит: "? i j" - повертає мінімальний елемент між i-им та j-им, включно;
зміна: "+ i x" - додати елемент x після i-го елементу списку.
Якщо i = 0, то елемент додається у початок масиву.
Звичайно ж, ця структура повинна бути достатньо хорошою.

Вхідні дані
Перший рядок містить кількість операцій n (1 ≤ n ≤ 200000) над масивом.
Наступні n рядків описують самі операції. Усі операції додавання є коректними.
Усі числа, що зберігаються у масиві, за модулем не перевищують 109.

Вихідні дані
Для кожної операції ? у окремому рядку виведіть її результат.
"""


class Element:

    def __init__(self, item):
        self.item = item
        self.next = None
        self.pre = None

    def __repr__(self):
        return "Element of list ({})".format(self.item)

    def __str__(self):
        return "Element of list ({})".format(self.item)


class BayonetList:

    def __init__(self):
        self._head = None
        self._end = None
        self._current = None

    def empty(self):
        return self._head is None and self._end is None

    def go_first(self):
        self._current = self._head

    def go_end(self):
        self._current = self._end

    def get_current(self):
        if self.empty():
            raise Exception("BayonetList: 'get_current' applied to empty container")
        else:
            return self._current.item

    def go_next(self):
        if self.empty():
            return Exception("BayonetList: 'go_next' applied to empty container")
        elif self._current.next is None:
            return Exception("BayonetList: 'go_next' applied out of range")
        else:
            self._current = self._current.next

    def go_pre(self):
        if self.empty():
            return Exception("BayonetList: 'go_pre' applied to empty container")
        elif self._current.next is None:
            return Exception("BayonetList: 'go_pre' applied out of range")
        else:
            self._current = self._current.pre

    def del_curr(self):
        if self.empty():
            return Exception("BayonetList: 'del_curr' applied to empty container")

        tmp = self._current
        tmp_pre = self._current.pre
        tmp_next = self._current.next

        if tmp_pre is not None:
            tmp_pre.next = tmp_next
        if tmp_next is not None:
            tmp_next.pre = tmp_pre
        del tmp
        self._current = None
        if not self.empty():
            self.go_first()

    def insert_after(self, item):
        tmp = Element(item)
        if self.empty():
            self._current = tmp
            self._head = tmp
            self._end = tmp
        else:
            tmp_next = self._current.next
            if tmp_next is not None:
                tmp_next.pre = tmp
                tmp.next = tmp_next
            tmp.pre = self._current
            self._current = tmp

    def insert_before(self, item):
        tmp = Element(item)
        if self.empty():
            self._head = tmp
            self._current = tmp
            self._end = tmp
        else:
            tmp_pre = self._current.pre
            if tmp_pre is not None:
                tmp_pre.next = tmp
                tmp.pre = tmp_pre
            tmp.next = self._current
            self._current.pre = tmp

    def __iter__(self):
        self.go_first()
        return self

    def __next__(self):
        if self.empty() or self._current is None:
            raise StopIteration
        self._current = self._current.next
        return self.get_current()

    def __str__(self):
        return "BayonetList(" + ' '.join(map(str, self)) + ')'

    def __repr__(self):
        return "BayonetList(" + ' '.join(map(str, self)) + ')'
