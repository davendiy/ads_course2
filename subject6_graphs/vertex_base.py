#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 21.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


class VertexBase:
    """ Базовий клас Vertex - вершина.

        Є базовим класом для класу, що описує вершину графа
        Клас містить поля - ключ (ім'я) вершини mId,
        а також її навантаження (тобто дані) mData.
    """

    def __init__(self, key):
        """ Конструктор створення вершини

        :param key: Ключ вершини
        """
        self.mKey = key    # Ключ (ім'я) вершини
        self.mData = None  # Навантаження (дані) вершини

    def key(self):
        """ Повертає ключ (ім'я) вершини

        :return: Ключ вершини
        """
        return self.mKey

    def set_data(self, data):
        """ Встановлює навантаження на вершину

        :param data: Навантаження
        :return: None
        """
        self.mData = data

    def data(self):
        """ Повертає навантаження вершини

        :return: Навантаження вершини
        """
        return self.mData

    def __str__(self):
        """ Зображення вершини у вигляді рядка """
        return str(self.mKey) + ": Data=" + str(self.data())
