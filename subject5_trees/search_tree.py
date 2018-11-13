#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from subject5_trees.binary_tree import BinaryTree


class SearchTree(BinaryTree):
    """ Клас - Бінарне дерево пошуку.

     Реалізує структуру даних, у якій вставка та пошук елементів здійснюється
     (в середньому) за логарифмічний час. """

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
        elif key < root.mKey:    # випадок: шуканий елемент може міститися у лівому піддереві
            return self._search_helper(root.mLeftChild, key) if root.hasLeft() else None
        else:                    # випадок: шуканий елемент може міститися у правому піддереві
            return self._search_helper(root.mRightChild, key) if root.hasRight() else None

    def insert(self, key):
        """ Метод, що реалізує вставку елемента у бінарне дерево

        :param key: ключ, що необхідно вставити
        """
        self._insert_helper(self, key)  # запускаємо вставку елемента key у дерево, починаючи з кореня

    def _insert_helper(self, root, key):
        """ Допоміжний рекурсиввий метод, для вставки заданого елемента у задане піддерево.

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

    def addItems(self, *items):
        """ Додає послідовність елементів у дерево пошуку

        :param items: Послідовність елементів, що додаються у дерево пошуку
        :return: None
        """
        for item in items:
            self.insert(item)


class SearchTreeWithDelete(SearchTree):
    """ Розширення класу бінарного дерева можливістю видаляти елементи """

    def delete(self, key):
        """ Видаляє заданий елемент у бінарному дереві

        :param key: Елемент, який потрібно видалити з бінарного дерева
        """
        self._delete_helper(self, key)

    def _search_max(self, root: SearchTree) -> SearchTree:
        """ Допоміжний рекурсивний метод пошуку найбільшого вузла у заданому піддереві.

            Згідно з властивостями бінарного дерева пошука, максимальний елемент може бути
            знайдений при проходженні дерева в глиб рухаючись лише по правих нащадках
        :param root: корінь піддерева у якому небхідно знайти найбільший вузол
        :return: знайдений вузол.
        """

        return self._search_max(root.mRightChild) if root.hasRight() else root

    def _delete_helper(self, root: SearchTree, key):
        """ Допоміжний рекурсиввий метод, що видаляє заданий елемент з дерева у заданому піддереві
            якщо такий елемент міситься у деремі. Пошук розпочинається з піддерева,
        що має коренем вершину startNode. Для технічних цілей передаємо у підпрограму
        предка вузла startNode - parent

        :param root: корінь піддерева у якому потрібно видалити заданий елемент
        :param key: Елемент, який потрібно видалити
        """

        node = self._search_helper(root, key)  # Знаходимо вузол, який треба видалити

        if node is None:  # Якщо шуканий елемент не міститься у дереві, то припиняємо роботу підпрограми
            return

        if node.hasNoChildren():      # Якщо знайдений вузол - листок (немає нащадків)
            if node.mParent is None:  # Якщо предок - корінь всього дерева
                node.mKey = None      # Робимо дерево порожнім
            else:
                if node.mParent.mLeftChild == node:
                    node.mParent.mLeftChild = None  # Видаляєм знайдений елемент
                else:
                    node.mParent.mRightChild = None  # Видаляєм знайдений елемент

        elif node.hasRight() and not node.hasLeft():  # Якщо знайдений вузол має лише одну праву гілку
            node.setNode(node.mRightChild)            # Замінюємо знайдений вузол його правим піддіревом

        elif node.hasLeft() and not node.hasRight():  # Якщо знайдений вузол має лише одну ліву гілку
            node.setNode(node.mLeftChild)             # Замінюємо знайдений вузол його лівим піддіревом

        else:                                             # Якщо знайдений вузол має обидві гілки
            left_max = self._search_max(node.mLeftChild)  # Знаходимо максимальний вузол у лівому піддереві
            left_max_key = left_max.mKey
            node.setNode(left_max_key)                    # Замінюємо значення елемета node знайденим максимальним
            self._delete_helper(node.mLeftChild, left_max_key)  # Видалення з лівого піддерева, найбільшого елементу


if __name__ == "__main__":
    t = SearchTree()
    t.addItems(12, 19, 8, 4, 10, 5, 21, 11, 15, 9, 1, 14, 16, 16)

    print(t)

    print(t.search(10))
    print(t.search(5))
    print(t.search(21))
    print(t.search(111))

    print()

    t = SearchTreeWithDelete()
    t.addItems(12, 19, 8, 4, 10, 5, 21, 11, 15, 9, 1, 14, 16, 16)
    t.delete(9)
    t.delete(10)
    t.delete(8)

    print()
