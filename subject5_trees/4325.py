#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

# TODO додебажити


class ErrorNotFoud(Exception):

    def __init__(self, index):
        Exception.__init__(self)
        self.index = index

    def __str__(self):
        return "there is no node with given index {}".format(self.index)


class Tree:
    """ Клас префіксне дерево."""

    _curr_index = -1

    def __init__(self, parent=None):
        """ Конструктор.
        Ініціалізує корінь дерева """
        Tree._curr_index += 1
        self.index = Tree._curr_index       # Ключ вершини дерева
        self.mData = None    # Навантаження вершини
        self.mChildren = []  # Список дітей дерева, місить пари {ребро: піддерево}
        self.parent = parent
        self.deep = parent.deep + 1 if parent is not None else 1

    def add_list(self, index, pos):
        node = self.find(index)
        if pos == 'l':
            node.mChildren.insert(0, Tree(parent=node))
        elif pos == 'r':
            node.mChildren.append(Tree(parent=node))
        else:
            for i, child in enumerate(node.mChildren):
                if child.index == pos:
                    node.mChildren.insert(i + 1, Tree(parent=node))
                    break

    def del_list(self, index):
        node = self.find(index)
        node.parent.mChildren.remove(node)
        del node

    def nodes_amount(self):
        res = 1
        for child in self.mChildren:
            res += child.nodes_amount()
        return res

    def find(self, index):
        """
        пошук синів
        :param index:
        :return:
        """
        res = None
        for el in self:
            if el.index == index:
                res = el
                break
        return res

    def find_way(self, index_from, index_to):
        node_from = self.find(index_from)
        node_to = self.find(index_to)
        if node_from.deep < node_to.deep:
            node_from, node_to = node_to, node_from
        res = 0

        while node_from.deep != node_to.deep:
            res += 1
            node_from = node_from.parent

        while node_from != node_to:
            res += 2
            node_from = node_from.parent
            node_to = node_to.parent
        res += 1
        return res

    def nodes_under(self, index_from, index_to):
        res = 0
        node_from = self.find(index_from)
        node_to = self.find(index_to)
        while node_from.deep > node_to.deep:
            if node_from == node_to:
                break
            k = node_from.parent.mChildren.index(node_from)
            for brother in node_from.parent.mChildren[k + 1:]:
                res += brother.nodes_amount
            node_from = node_from.parent

        while node_from.deep < node_to.deep:
            if node_from == node_to:
                break
            k = node_to.parent.mChildren.index(node_to)
            for brother in node_to.parent.mChildren[:k]:
                res += brother.nodes_amount()
            node_to = node_to.parent

        for i in range(node_to.deep):
            if node_from == node_to:
                break
            parent_from = node_from.parent
            parent_to = node_to.parent
            k1 = parent_from.mChildren.index(node_from)
            k2 = parent_to.mChildren.index(node_to)
            if parent_from == parent_to:
                for brother in parent_to.mChildren[k1 + 1: k2]:
                    res += brother.nodes_amount()
                break

            for brother in parent_from.mChildren[k1 + 1:]:
                res += brother.nodes_amount()
            for brother in parent_to.mChildren[:k2]:
                res += brother.nodes_amount()
            node_to = parent_to
            node_from = parent_from
        return res

    def __str__(self):
        tmp1 = self.parent.index if self.parent is not None else 0
        tmp2 = [child.index for child in self.mChildren]
        return "Node(index={}," \
               " deep={}, " \
               "parent={}, " \
               "children: {})".format(self.index, self.deep, tmp1, tmp2)

    def __repr__(self):
        tmp1 = self.parent.index if self.parent is not None else 0
        tmp2 = [child.index for child in self.mChildren]
        return "Node(index={}," \
               " deep={}, " \
               "parent={}, " \
               "children: {})".format(self.index, self.deep, tmp1, tmp2)

    def __iter__(self):
        yield self
        for child in self.mChildren:
            for child2 in child:
                yield child2


if __name__ == '__main__':

    with open('input.txt', 'r') as file:
        with open('output.txt', 'w') as outfile:
            test = Tree()
            file.readline()
            for line in file:
                tmp = line.split()
                if tmp[0] in 'lr':
                    test.add_list(int(tmp[1]), tmp[0])
                elif tmp[0] == 'a':
                    test.add_list(int(tmp[1]), int(tmp[2]))
                elif tmp[0] == 'd':
                    test.del_list(int(tmp[1]))
                elif tmp[0] == 'p':
                    outfile.write(str(test.find_way(int(tmp[1]), int(tmp[2]))) + '\n')
                elif tmp[0] == 'q':
                    outfile.write(str(test.nodes_under(int(tmp[1]), int(tmp[2]))) + '\n')
