#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class Heap:
    """ Клас структура даних Купа """

    __slots__ = ('mItems', 'mSize')

    def __init__(self):
        """ Конструктор """
        self.mItems = [0]
        self.mSize = 0

    def empty(self):
        """ Перевіряє чи купа порожня

        :return: True, якщо купа порожня
        """
        return len(self.mItems) == 1

    def insert(self, *k):
        """ Вставка елемента в купу

        :param k: k[0] - Елемент, що вставляється у купу
        """
        self.mSize += 1
        self.mItems.append(k[0])  # Вставляємо на останню позицію,
        self.siftUp()  # просіюємо елемент вгору

    def getMaximum(self):
        return self.mItems[1] if len(self.mItems) > 1 else 0

    def extractMaximum(self):
        """ Повертає мінімальний елемент кучі

        :return: Мінімальний елемент кучі
        """
        root = self.mItems[1]  # Запам'ятовуємо значення кореня дерева
        self.mItems[1] = self.mItems[-1]  # Переставляємо на першу позицію останній елемент (за номером) у купі
        self.mItems.pop()  # Видаляємо останній (за позицією у масиві) елемент купи
        self.mSize -= 1

        self.siftDown()  # Здійснюємо операцію просіювання вниз, для того,
        # щоб опустити переставлений елемент на відповідну позицію у купі

        return root  # повертаємо значення кореня, яке було запам'ятовано на початку

    def siftDown(self):
        """ Просіювання вниз """
        i = 1
        while (2 * i + 1) <= self.mSize:
            left = 2 * i
            right = 2 * i + 1
            min_child = self.maxChild(left, right)
            if self.mItems[i][0] < self.mItems[min_child][0] or \
                    (self.mItems[i][0] == self.mItems[min_child][0] and
                     self.mItems[i][1] > self.mItems[min_child][1]):
                self.swap(min_child, i)
            i = min_child

    def siftUp(self):
        """ Дпопоміжний метод просіювання вгору """
        i = len(self.mItems) - 1
        while i > 1:
            parent = i // 2
            if self.mItems[i][0] > self.mItems[parent][0]:
                self.swap(parent, i)
            elif self.mItems[i][0] == self.mItems[parent][0] and \
                    self.mItems[i][1] < self.mItems[parent][1]:
                self.swap(parent, i)
            i = parent

    def swap(self, i, j):
        """ Допоміжний метод для перестановки елементів у купі,
        що знаходяться на заданих позиціях i та j

        :param i: перший індекс
        :param j: другий індекс
        """
        self.mItems[i], self.mItems[j] = self.mItems[j], self.mItems[i]

    def maxChild(self, left_child, right_child):
        """ Допоміжна функція знаходження меншого (за значенням) вузла серед нащадків поточного

        :param left_child: лівий син
        :param right_child: правий син
        :return: менший з двох синів
        """
        if right_child < self.mSize:
            return left_child
        else:
            if self.mItems[left_child] > self.mItems[right_child]:
                return left_child
            else:
                return right_child


class PriorityQueue(Heap):
    __slots__ = Heap.__slots__ + ('mElementMap',)

    def __init__(self):
        Heap.__init__(self)
        self.mElementMap = {}

    def insert(self, *k):
        k = k[0]
        priority = self.mElementMap.get(k, None)
        if priority is None:
            self.mElementMap[k] = 1
            Heap.insert(self, (1, k))
        else:
            self.mElementMap[k] += 1
            Heap.insert(self, (priority + 1, k))

    def extractMaximum(self):
        res = Heap.extractMaximum(self)  # type: tuple
        self.mElementMap[res[1]] -= 1
        return res
    #
    # def __str__(self):
    #     return f'PriorityQueue({self.mItems})'
    #
    # def __repr__(self):
    #     return f'PriorityQueue({self.mItems})'


if __name__ == '__main__':
    n = int(input())
    task = PriorityQueue()
    for count in range(n):
        tmp = input().split()
        if tmp[0] == '+':
            task.insert(int(tmp[1]))
            rez = task.getMaximum()
            rez = rez if rez == 0 else rez[1]
            print(rez)
        else:
            task.extractMaximum()
            rez = task.getMaximum()
            rez = rez if rez == 0 else rez[1]
            print(rez)
