#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class Node:
    """ Допоміжний клас, що реалізує вузол стеку """

    def __init__(self, item):
        """ Конструктор

        :param item: навантаження вузла
        """
        self.item = item   # створюєм поле для зберігання навантаження
        self.next = None   # посилання на наступний вузол стеку

    def __del__(self):
        del self.item
        del self.next
    #
    # def __str__(self):
    #     if self.next is not None:
    #         tmp = self.next.item
    #     else:
    #         tmp = None
    #     return 'Node({}, {})'.format(self.item, tmp)
    #
    # def __repr__(self):
    #     if self.next is not None:
    #         tmp = self.next.item
    #     else:
    #         tmp = None
    #     return 'Node({}, {})'.format(self.item, tmp)


class Stack:
    """ Клас, що реалізує стек елементів
        як рекурсивну структуру """

    def __init__(self):
        """ Конструктор
        """
        self.top_node = None  # посилання на верхівку стеку
        self._now_node = None

    def empty(self):
        """ Перевіряє чи стек порожній

        :return: True, якщо стек порожній
        """
        return self.top_node is None

    def push(self, item):
        """ Додає елемент у стек

        :param item: елемент, що додається у стек
        :return: None
        """

        new_node = Node(item)              # Створюємо новий вузол стеку
        if not self.empty():               # Якщо стек не порожній, то новий вузол
            new_node.next = self.top_node  # має посилатися на поточну верхівку

        self.top_node = new_node  # змінюємо верхівку стека новим вузлом

    def pop(self):
        """ Забирає верхівку стека
            Сам вузол при цьому прибирається зі стеку

        :return: Навантаження верхівки стеку
        """
        if self.empty():   # Якщо стек порожній
            raise Exception("Stack: 'pop' applied to empty container")

        current_top = self.top_node         # запам'ятовуємо поточну верхівку стека
        item = current_top.item             # запам'ятовуємо навантаження верхівки
        self.top_node = self.top_node.next  # замінюємо верхівку стека наступним вузлом у стеці
        del current_top  # видаляємо запам'ятований вузол, що місить попередню верхівку стека

        return item

    def top(self):
        """ Повертає верхівку стека
            Сам вузол при цьому лишається у стеці

        :return: Навантаження верхівки стеку
        """

        if self.empty():
            raise Exception("Stack: 'top' applied to empty container")
        return self.top_node.item

    def __iter__(self):
        """ Ітератор по стеку
            Повертає сам себе, але створює лічильник
        """
        self._now_node = Node(None)
        self._now_node.next = self.top_node
        return self

    def __next__(self):
        if self._now_node.next is None:
            self._now_node = None
            raise StopIteration
        else:
            self._now_node = self._now_node.next
            return self._now_node.item


class StackWithMin(Stack):

    def __init__(self):
        Stack.__init__(self)
        self._min = None

    def push(self, item):
        if self._min is None or (item < self._min and self._min is not None):
            self._min = item
        Stack.push(self, item)

    def _update_min(self):
        self._min = None
        for el in self:
            if self._min is None:
                self._min = el
                continue
            if el < self._min:
                self._min = el

    def pop(self):
        tmp = Stack.pop(self)
        if tmp == self.min:
            self._update_min()
        return tmp

    @property
    def min(self):
        return self._min


def task():
    with open('output.txt', 'w') as out_file:
        with open('input.txt', 'r') as file:
            test = StackWithMin()
            t = True
            for line in file:
                if t:
                    t = False
                    continue
                tmp = list(map(int, line.split()))
                if tmp[0] == 1:
                    test.push(tmp[1])
                elif tmp[0] == 2:
                    test.pop()
                else:
                    tmp_min = test.min
                    out_file.write(str(tmp_min) + '\n')


if __name__ == '__main__':
    # test = Stack()
    # test.push(2)
    # test.push(2)
    # test.push(3)
    # test.push(4)
    # test.push(5)
    # test.push(1)
    # test.push(2)
    # print(list(test))
    #
    # test.del_min()
    #
    # print(list(test))

    task()
