#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def gt_tuple(tuple1, tuple2):
    return tuple1[0] > tuple2[0] or (tuple1[0] == tuple2[0] and tuple1[1] < tuple2[1])


def lt_tuple(tuple1, tuple2):
    return tuple1[0] < tuple2[0] or (tuple1[0] == tuple2[0] and tuple1[1] > tuple2[1])


class AVLTree:

    __slots__ = ('mKey', 'mLeftChild', 'mRightChild', 'mParent', 'height')

    def __init__(self, key=None, left=None, right=None):
        """ Перевизначення конструктора
            Реалізує створення AVL дерева з будь-якого нащадка BinaryTree, або
            просто з параметрами key, left, right

        :param key: ключ
        :param left: лівий син
        :param right: правий син
        """
        self.mKey = key  # ключ кореня дерева
        self.mLeftChild = None  # поле для лівого сина
        self.mRightChild = None  # поле для правого сина
        self.mParent = None  # поле для батька поточного вузла

        if left is not None:
            self.setLeft(left)  # встановлюємо лівого сина
        if right is not None:
            self.setRight(right)  # встановлюємо правого сина

        self.height = 0

    def empty(self) -> bool:
        """ Перевіряє чи дерево порожнє, тобто чи має воно навантаження та дітей

        :return: True, якщо дерево немає ключа та дітей
        """
        return (self.mKey is None
                and self.mLeftChild is None
                and self.mRightChild is None)

    def hasLeft(self) -> bool:
        """ Чи містить дерево лівого сина

        :return: True, якщо дерево має лівого сина.
        """
        return self.mLeftChild is not None

    def hasRight(self) -> bool:
        """ Чи містить дерево правого сина

        :return: True, якщо дерево має правого сина.
        """
        return self.mRightChild is not None

    def max(self):
        if self.hasRight():
            return self.mRightChild.max()
        else:
            return self.mKey

    def fixHeight(self):
        """ Перерахування висоти дерева

        """
        self.height = 1 + max(self.mRightChild.height if self.hasRight() else 0,
                              self.mLeftChild.height if self.hasLeft() else 0)

    def setNode(self, item):
        """ Змінює поточний вузол

        :param item: Нове піддерево або ключ
        :return: None
        """
        if isinstance(item, AVLTree):         # якщо item є деревом
            self.mKey = item.mKey                # змінюємо ключ
            self.mLeftChild = item.mLeftChild    # змінюємо ліве піддерево
            self.mRightChild = item.mRightChild  # змінюємо праве піддерево
        else:
            self.mKey = item
        self.fixHeight()             # перераховуємо висоту

    def setLeft(self, item):
        """ Перевизначення оригінального setLeft
            Змінює лівого сина.
            Якщо дерево не має сина, то створюємо не BinaryTree, а AVLTree

        :param item: Навантаження або піддерево
        :return: None_dfs
        """
        if isinstance(item, AVLTree):        # якщо item є деревом
            self.mLeftChild = item              # змінюємо все піддерево
        elif self.hasLeft():                    # якщо дерево містить лівого сина
            self.mLeftChild.setNode(item)       # замінюємо вузол
        else:                                   # якщо дерево немає лівого сина
            self.mLeftChild = AVLTree(item)  # створюємо дерево з вузлом item та робимо його лівим сином

        self.mLeftChild.mParent = self
        self.fixHeight()            # перераховуємо висоту

    def setRight(self, item):
        """ Перевизначення оригінального setRight
            Змінює правого сина
            Якщо дерево не має сина, то створюємо не BinaryTree, а AVLTree

        :param item: Ключ або піддерево
        :return: None
        """
        if isinstance(item, AVLTree):         # якщо item є деревом
            self.mRightChild = item              # змінюємо все піддерево
        elif self.hasRight():                    # якщо дерево містить правого сина
            self.mRightChild.setNode(item)       # замінюємо вузол
        else:                                    # якщо дерево немає правого сина
            self.mRightChild = AVLTree(item)  # створюємо дерево з вузлом item та робимо його правим сином

        self.mRightChild.mParent = self
        self.fixHeight()

    def search(self, key):
        """ Метод, що реалізує пошук елемента item у бінарному дереві

        :param key: Шуканий елемент
        :return: Вузол з ключем key якщо такий елемент міститься у дереві та None - якщо елемент не знайдений.
        """
        return self._search_helper(self, key)  # запускаємо пошук вузла з ключем key у дереві, починаючи з кореня

    def _search_helper(self, root, key):
        """ Допопоміжний рекурсиввий метод, для пошуку елементу у заданому піддереві.

        Пошук здійснюється проходом в глибину.
        :param root: корінь піддерева у якому здійснюється пошук
        :param key: Шуканий елемент
        :return: посилання на знайдений елемент, якщо елемент міститься у дереві та None - якщо елемент не знайдений.
        """
        if root.empty():             # якщо піддерево sub_tree порожнє,
            return None              # а отже вузол не знайдено - повертаємо None

        if root.mKey == key:     # якщо ключ поточного вузла збігається з шуканим,
            return root          # повертаємо знайдений вузол
        elif lt_tuple(key, root.mKey):    # випадок: шуканий елемент може міститися у лівому піддереві
            return self._search_helper(root.mLeftChild, key) if root.hasLeft() else None
        else:                    # випадок: шуканий елемент може міститися у правому піддереві
            return self._search_helper(root.mRightChild, key) if root.hasRight() else None

    @staticmethod
    def _singleLeftRotate(root):
        """ Малий лівий поворот бінарного дерева

        :param root: корінь
        """
        if not root.hasRight():         # якщо нема правого сина, то поворот неможливий
            return

        b = root.mRightChild         # запам'ятовуємо правого сина в окремій змінні
        root.mRightChild = None      # видаляємо показчик на нього

        c = b.mLeftChild             # лівий син правого сина - піддерево Central в алгоритмі
        if c is not None:
            root.setRight(c)         # якщо він не None, то робимо його правим сином кореня через стандартну фунцкію
        else:
            root.mRightChild = None  # інакше примусово присваюємо None, оскільки стандартний створює пусте піддерево

        a = AVLTree(root.mKey, root.mLeftChild, root.mRightChild)   # запам'ятовування кореня в окремій змінній
        root.setNode(b)              # зміна кореня на його правого сина
        root.setLeft(a)              # робимо корінь лівим сином b

        root.mLeftChild.fixHeight()  # перераховуємо висоту лівого сина і кореня, т.к. вони зміняться
        root.fixHeight()

    @staticmethod
    def _singleRightRotate(root):
        """ Малий правий поворот бінарного дерева
            Аналогічний малому лівому

        :param root: корінь
        """
        if not root.hasLeft():
            return

        b = root.mLeftChild
        root.mLeftChild = None

        c = b.mRightChild
        if c is not None:
            root.setLeft(c)
        else:
            root.mLeftChild = None
        a = AVLTree(root.mKey, root.mLeftChild, root.mRightChild)
        root.setNode(b)
        root.setRight(a)

        root.mRightChild.fixHeight()
        root.fixHeight()

    def _balance(self, root):
        """ Балансування піддерева

        :param root: корінь піддерева
        """

        if root.bFactor == 2:      # якщо переважає права вершина на 2, то треба зробити малий лівий поворот
            if root.hasRight() and root.mRightChild.bFactor < 0:   # якщо ще середня частина більша за праву,
                self._singleRightRotate(root.mRightChild)                  # то необхідно зробити великий лівий поворот,
            self._singleLeftRotate(root)                                   # який скл з 2-х малих

        if root.bFactor == -2:     # аналогічно, якщо переважає ліва вершина
            if root.hasLeft() and root.mLeftChild.bFactor > 0:
                self._singleLeftRotate(root.mLeftChild)
            self._singleRightRotate(root)

    def insert(self, key):
        self._insert_helper(self, key)

    def _insert_helper(self, root, key):
        """ Перевизначення допоміжного рекурсивного методу класа-предка для коректної роботи
            АВЛ дерева. Єдина відмінність - балансування вершини перед виходом з рекурсії.
            Допоміжний рекурсиввий метод, для вставки заданого елемента у задане піддерево.

        :param root: корінь піддерева у яке відбувається вставка нового елементу
        :param key: Елемент для вставки
        """

        if root.empty():                # якщо піддерево з коренем startNode порожнє
            root.setNode(key)           # вставляємо елемент item
        else:

            if lt_tuple(key, root.mKey):         # якщо елемент для вставки має міститися у лівому піддереві
                if root.hasLeft():      # якщо дерево має лівого нащадка
                    #  запускаємо рекурсивно вставку item у ліве піддерево
                    self._insert_helper(root.mLeftChild, key)
                else:                   # якщо дерево не має лівого нащадка
                    root.setLeft(key)   # додаємо item у ролі лівого нащадка

            elif gt_tuple(key, root.mKey):        # якщо елемент для вставки має міститися у правому піддереві
                if root.hasRight():      # якщо дерево має правого нащадка
                    #  запускаємо рекурсивно вставку item у праве піддерево
                    self._insert_helper(root.mRightChild, key)
                else:                        # якщо дерево не має правого нащадка
                    root.setRight(key)  # додаємо item у ролі правого нащадка
        root.fixHeight()
        self._balance(root)

    def delete(self, item):
        """ Видалення елемента з AVL дерева

        :param item: ключ елемента
        """
        if item == self.mKey:
            self.setNode(self._delete_helper(self, item))
        else:
            self._delete_helper(self, item)

    def _pop_min2(self, root):
        """ Рекурсивне видалення мінімального елемента в піддереві

        :param root: корінь піддерева
        :return: мінімальний елемент, піддерево, яке лишилось
        """
        if root.hasLeft():                                      # якщо в кореня є лівий син
            find_min, child = self._pop_min2(root.mLeftChild)   # рекурсивно запускаємо функцію для сина
            root.mLeftChild = child                             # робимо лівим сином піддерево, яке лишилось
            if child is not None:           # якщо піддерево, яке лишилось, не пусте, то треба йому поміняти батька
                child.mParent = root
            root.fixHeight()                # балансування
            self._balance(root)
            return find_min, root
        else:
            right = root.mRightChild        # якщо лівого сина нема - то елемент є мінімальним
            root.mRightChild = None         # повертаємо його самого і його правого сина
            return root, right

    def _delete_helper(self, root, item):
        """ Рекурсивне видалення елемента у піддереві

        :param root: корінь піддерева
        :param item: ключ елемента
        :return: змінене піддерево
        """
        if root.mKey == item:               # якщо знайшли необхідний елемент
            res = root.mLeftChild           # запам'ятовуємо його синів
            root.mLeftChild = None

            right = root.mRightChild
            root.mRightChild = None

            # якщо правий син не None, то треба поміняти шуканий елемент
            # з мінімальним у правому піддереві
            if right is not None:
                min_right, right = self._pop_min2(right)  # вилучення мінімального з правого піддерева
                min_right.mRightChild = right             # робимо праве піддерево правим сином мінімального
                if right is not None:
                    right.mParent = min_right
                min_right.mLeftChild = res                # а ліве піддерево шуканого елемента лівим сином мінімального
                if res is not None:
                    res.mParent = min_right
                res = min_right

            res, root = root, res    # міняємо показчики на корінь і на результуюче піддерево,
            del res                  # щоб обійтись одним гарним return в кінці функції + видаляємо наш самотній елемент

        elif gt_tuple(item, root.mKey) and root.hasRight():        # якщо ключ більший, то рекурсивно запускаємо функцію
            res = self._delete_helper(root.mRightChild, item)    # для правого сина
            root.mRightChild = res                               # міняємо правого сина на результуючого
            if res is not None:
                res.mParent = root

        elif lt_tuple(item, root.mKey) and root.hasLeft():        # аналогічно, якщо менший
            res = self._delete_helper(root.mLeftChild, item)
            root.mLeftChild = res
            if res is not None:
                res.mParent = root           # якщо нема синів, то повертаємо корінь

        if root is not None:          # балансування зміненого піддерева (відбуватиметься кожен раз при виході з
            root.fixHeight()          # рекурсії)
            self._balance(root)
        return root

    @property
    def bFactor(self) -> int:
        """ Balance factor (різниця висот правого і лівого синів)
        :return: ціле число
        """
        right_height = self.mRightChild.height if self.hasRight() else 0
        left_height = self.mLeftChild.height if self.hasLeft() else 0
        return right_height - left_height

    def __iter__(self):
        """ Ітератор по дереву в глибину

        """
        return self._dfs(self, 0)

    def _dfs(self, root, deep: int) -> tuple:
        """ обхід дерева в глибину

        :param deep: глибина у даний момент
        :return: вершина, її глибина
        """
        yield root, deep

        if root.hasLeft():
            for node in self._dfs(root.mLeftChild, deep + 1):
                yield node

        if root.hasRight():
            for node in self._dfs(root.mRightChild, deep + 1):
                yield node


if __name__ == '__main__':

    elements_amount = {}
    tree = AVLTree()
    n = int(input())
    for i in range(n):

        tmp = input().split()
        element = int(tmp[1])
        if tmp[0] == '+':
            if element in elements_amount:
                amount = elements_amount[element]
                elements_amount[element] += 1
                tree.delete((amount, element))
                tree.insert((amount+1, element))
            else:
                elements_amount[element] = 1
                tree.insert((1, element))
        else:
            amount = elements_amount[element]
            tree.delete((amount, element))
            elements_amount[element] -= 1
            if amount-1 > 0:
                tree.insert((amount-1, element))
        if tree.empty():
            print(0)
        else:
            print(tree.max()[1])

        # print(" ".join(str(root.mKey) for root, deep in tree))

    # import random
    # tree = AVLTree()
    # elements_amount = {}
    # for i in range(10000):
    #     element = random.randrange(10000)
    #     if element in elements_amount:
    #         amount = elements_amount[element] + 1
    #         elements_amount[element] = amount
    #     else:
    #         elements_amount[element] = 1
    #         amount = 1
    #     tree.insert((amount, element))
    #
    # for i in range(10000):
    #     element = random.randrange(10000)
    #     if element in elements_amount:
    #         amount = elements_amount[element]
    #         tree.delete((amount, element))
    #         if amount-1 > 0:
    #             elements_amount[element] = amount - 1
    #         else:
    #             del elements_amount[element]
