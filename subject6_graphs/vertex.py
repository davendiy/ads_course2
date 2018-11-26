#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 21.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from subject6_graphs.vertex_base import VertexBase
import sys

INF = sys.maxsize


class Vertex(VertexBase):

    def __init__(self, key):
        """ Конструктор створення вершини

        :param key: Ключ вершини
        """
        super().__init__(key)  # Викликаємо конструктор батьківського класу
        self.mNeighbors = {}  # Список сусідів вершини у вигляді пар (ім'я_сусіда: вага_ребра)

    def add_neighbor(self, vertex, weight=1):
        """ Додати сусіда

        Додає ребро, що сполучає поточну вершину з вершиною Vertex з вагою weight
        Vertex може бути або іншою вершиною, тобто об'єктом класу Vertex
        або ключем (ідентифікатором вершини)
        :param vertex: Вершина-сусід або ключ вершини
        :param weight: Вага ребра
        :return: None
        """
        if isinstance(vertex, VertexBase):  # Якщо Vertex - вершина
            self.mNeighbors[vertex.key()] = weight
        else:  # Якщо Vertex - ім'я (ключ) вершини
            self.mNeighbors[vertex] = weight

    def neighbors(self):
        """ Повертає список ключів всіх сусідів поточної вершини

        :return: Список ключів всіх сусідів вершини
        """
        return self.mNeighbors.keys()

    def weight(self, neighbor):
        """ Повертає вагу ребра, що сполучає поточну вершину та вершину-сусіда

        :param neighbor: Вершина-сусід
        :return: Вага ребра
        """
        if isinstance(neighbor, VertexBase):  # Якщо aNeighbor - вершина (не ім'я)
            return self.mNeighbors[neighbor.key()]
        else:  # Якщо aNeighbor - ім'я (ключ) сусідньої вершини
            return self.mNeighbors[neighbor]

    def __str__(self):
        """ Зображення вершини у вигляді рядка у разом з усіма її сусідами """
        return super().__str__() + ' connected to: ' + str(self.mNeighbors)


class VertexForAlgorithms(Vertex):
    """ Клас, що є розширенням класу для вершини графа

        Використовується у алгоритмах Белмана-Форда, Дейкстри, А*...
        Міститть додаткову технічну інформацію, що необхідна для реалізації щих алгоритмів
     """

    def __init__(self, key):
        """ Конструктор створення вершини

        :param key: Ключ вершини
        """
        super().__init__(key)

        # Відтань - додаткове навантаження на вершину - величина найкоротшого шляху
        # від деякої фіксованої вершини до поточної вершини графа.
        # Використовується для хвильового алгоритму, алгоритмів Дейкстри, Белмана-Форда та ін.
        self.mDistance = INF  # До початку роботи алгортиму вважаємо, що вона є несінченністю!

        # Джерело - додаткове навантаження на вершину -
        # вершина з якої прийшли по найкорошому шляху
        # у поточну вернишу на деякому кроці алгоритму
        self.mSource = None  # До початку роботи алгортиму вважаємо, що вона є невизначеною

    def set_distance(self, distance):
        """ Встановлює відстань для поточної вершини

        :param distance: Нова відстань
        :return: None
        """
        self.mDistance = distance

    def distance(self):
        """ Повератє поточну відстань у вершині)

        :return: Відстань у вершині
        """
        return self.mDistance

    def set_source(self, source):
        """ Встанолює джерело для поточної вершини

        :param source: Нове джерело вершини
        :return: None
        """
        self.mSource = source

    def source(self):
        """ Повертає джерело для поточної вершини

        :return: Джерело поточної вершини
        """
        return self.mSource

    def visited(self):
        """ Чи відвідана вершина на поточному кроці алгоритму
        Якщо вершина була принаймні один раз відвідана, то відстань у ній менша за нескінченність

        :return: True, якщо вершина була відвідана на поточному кроці алгоритму
        """
        return self.mDistance != INF

    def set_unvisited(self):
        """ Встановлює відстань у поточній вершині як нескінченність

        :return: None
        """
        self.mDistance = INF

    def __str__(self):
        """ Зображення вершини у вигляді рядка у разом з усіма її сусідами """
        return str(self.mKey) + ": Data = " + str(self.data()) + "  Dist = " + str(self.mDistance) + "  From: " \
               + str(self.mSource) + ' connected: ' + str(self.mNeighbors)
        # return str(self.mId) + ": Data=" + str(self.getData())


if __name__ == "__main__":
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)

    v1.add_neighbor(v1, 11)
    v1.add_neighbor(v2, 22)
    v1.add_neighbor(v3, 33)

    print(v1)
    print(v2)
    print(v3)

    print(v1.weight(v2))
