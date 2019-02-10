#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from subject5_trees.search_tree import SearchTree, BinaryTree


def _dfs(bin_tree: BinaryTree):
    """ Обхід бінарного дерева в глибину

    """
    yield bin_tree

    if bin_tree.hasLeft():
        for node in _dfs(bin_tree.mLeftChild):
            yield node

    if bin_tree.hasRight():
        for node in _dfs(bin_tree.mRightChild):
            yield node


class AVLTree(SearchTree):

    def __init__(self, key=None, left=None, right=None):
        """ Перевизначення конструктора
            Реалізує створення AVL дерева з будь-якого нащадка BinaryTree, або
            просто з параметрами key, left, right

        :param key: ключ
        :param left: лівий син
        :param right: правий син
        """
        if isinstance(key, BinaryTree):    # якщо ключем є нащадок бінарного дерева:
            super().__init__()             # створюємо пусте бінарне, тільки додаємо атрибут height
            self.height = 0
            self._fromBinary(key)          # заповнюємо його елементами з бінарного берева
        else:
            super().__init__(key, left, right)  # інакше - створюємо його як бінарне з новим атрибутом
            self.height = 0
        self.fixHeight()

    def _fromBinary(self, bin_tree):
        """ Заповнення авл-дерева елементами бінарного

        :param bin_tree: нащадок бінарного дерева
        """
        if hasattr(bin_tree, '__iter__'):     # якщо в класі реалізовано власна ітерація - користуємося нею
            for el in bin_tree:
                if isinstance(el, BinaryTree):     # перевірка типу, який видає ітератор
                    self.insert(el.mKey)
                else:
                    self.insert(el)
        else:
            for el in _dfs(bin_tree):         # якщо ж не реалізовано, то обходимо дерево в глибину
                self.insert(el.mKey)

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
        if isinstance(item, BinaryTree):         # якщо item є деревом
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
        if isinstance(item, BinaryTree):        # якщо item є деревом
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
        if isinstance(item, BinaryTree):         # якщо item є деревом
            self.mRightChild = item              # змінюємо все піддерево
        elif self.hasRight():                    # якщо дерево містить правого сина
            self.mRightChild.setNode(item)       # замінюємо вузол
        else:                                    # якщо дерево немає правого сина
            self.mRightChild = AVLTree(item)  # створюємо дерево з вузлом item та робимо його правим сином

        self.mRightChild.mParent = self
        self.fixHeight()

    def singleRotate(self, key, direction: int):
        """ Реалізує малий поворот

        :param key: вузол для якого треба зробити поворот
        :param direction: напрямок {1 - правий, -1 - лівий)
        """
        node = self.search(key)           # type: AVLTree
        if node is not None and direction == -1:
            self._singleLeftRotate(node)
        elif node is not None:
            self._singleRightRotate(node)

    def doubleRotate(self, key, direction: int):
        """ Реалізує великий поворот

        :param key: вузол, який треба повернути
        :param direction: напрямок (1 - правий, -1 - лівий)
        """
        node = self.search(key)   # type: AVLTree

        if node is None:
            return
        elif direction == -1:              # великий поворот складається з 2-х малих
            if node.hasRight():
                self._singleRightRotate(node.mRightChild)
            self._singleLeftRotate(node)
        else:
            if node.hasLeft():
                self._singleLeftRotate(node.mLeftChild)
            self._singleRightRotate(node)

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

            if key < root.mKey:         # якщо елемент для вставки має міститися у лівому піддереві
                if root.hasLeft():      # якщо дерево має лівого нащадка
                    #  запускаємо рекурсивно вставку item у ліве піддерево
                    self._insert_helper(root.mLeftChild, key)
                else:                   # якщо дерево не має лівого нащадка
                    root.setLeft(key)   # додаємо item у ролі лівого нащадка

            elif key > root.mKey:        # якщо елемент для вставки має міститися у правому піддереві
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

        elif item > root.mKey and root.hasRight():         # якщо ключ більший, то рекурсивно запускаємо функцію
            res = self._delete_helper(root.mRightChild, item)    # для правого сина
            root.mRightChild = res                               # міняємо правого сина на результуючого
            if res is not None:
                res.mParent = root

        elif item < root.mKey and root.hasLeft():        # аналогічно, якщо менший
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

    def __str__(self):
        """ Зображення дерева у вигляді рядка

        """
        tmp1 = self.mLeftChild.mKey if self.hasLeft() else None
        tmp2 = self.mRightChild.mKey if self.hasRight() else None
        tmp3 = self.mParent if self.mParent is None else self.mParent.mKey
        return "AVLTree(key={}, left={}, right={}, parent={}, height={})".format(self.mKey, tmp1, tmp2,
                                                                                 tmp3, self.height)

    def __repr__(self):
        """ Зображення дерева у вигляді рядка

        """
        tmp1 = self.mLeftChild.mKey if self.hasLeft() else None
        tmp2 = self.mRightChild.mKey if self.hasRight() else None
        tmp3 = self.mParent if self.mParent is None else self.mParent.mKey
        return "AVLTree(key={}, left={}, right={}, parent={}, height={})".format(self.mKey, tmp1, tmp2,
                                                                                 tmp3, self.height)


def print_BFS(root: BinaryTree):
    """ Обхід бінарного дерева в ширину

    :param root: Корінь бінарного дерева
    """
    q = [root]
    while q:
        next_q = []
        for el in q:
            print(el, end=' ')

            if el.hasLeft():
                next_q.append(el.mLeftChild)
            if el.hasRight():
                next_q.append(el.mRightChild)
        print()
        q = next_q


if __name__ == '__main__':
    arr = (2, 0, -1, 5, 1, 3, 6, 2.5, 4, 2.3, 4.5)
    print("масив:", arr)
    test = SearchTree()
    test.addItems(*arr)
    print("Звичайне дерево пошуку:")
    print_BFS(test)
    print("\nAVL дерево:")
    test = AVLTree(test)
    print_BFS(test)
    print()

    print("del 3")
    test.delete(3)
    print_BFS(test)
    print()

    arr = tuple(range(20))
    print("масив:", arr)
    test = AVLTree()
    test.addItems(*arr)
    print_BFS(test)
    print()

    print('del 11')
    test.delete(11)
    print_BFS(test)
    print()
