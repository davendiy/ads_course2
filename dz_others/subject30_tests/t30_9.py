#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import unittest


class Section:

    def __init__(self, a, b):
        self._empty = a >= b
        if self._empty:
            self.start = 0
            self.end = 0
        else:
            self.start = a
            self.end = b

    def do_empty(self):
        """ Зробити відрізок пустим
        """
        self.start = 0
        self.end = 0
        self._empty = True

    def equate(self, a, b):
        """ Покласти відрізок рівним a, b

        Якщо a >= b, то відрізок є порожнім
        :param a: дійсне число
        :param b: дійсне число
        """
        self.start = a
        self.end = b
        if a >= b:
            self.do_empty()

    def isempty(self):
        """ Перевірка, чи є відрізок порожнім
        """
        return self._empty

    def intersection(self, t1, t2):
        """ Покласти відрізок рівним перетину t1 i t2

        :param t1: Section
        :param t2: Section
        """
        self.equate(max(t1.start, t2.start), min(t1.end, t2.end))


class TestSection(unittest.TestCase):

    def testInit(self):

        test = Section(0, 1)
        self.assertTrue(test.isempty(), False)
        self.assertTrue(test.start, 0)
        self.assertTrue(test.end, 1)

        test = Section(0, -1)
        self.assertTrue(test.isempty(), True)

        test = Section(0, 0)
        self.assertTrue(test.isempty(), True)

    def testDoEmpty(self):

        test = Section(0, 20)
        test.do_empty()
        self.assertTrue(test.isempty(), True)
        self.assertTrue(test.start, 0)
        self.assertTrue(test.end, 0)

    def testEqual(self):
        test = Section(0, 2)

        test.equate(2, 5)
        self.assertTrue(test.start, 2)
        self.assertTrue(test.end, 5)
        self.assertTrue(test.isempty(), False)

        test.equate(4, 1)
        self.assertTrue(test.isempty(), True)

    def testIntersection(self):

        test = Section(0, 2)
        test1 = Section(4, 8)
        test2 = Section(0, 1)

        test.intersection(test1, test2)
        self.assertTrue(test.isempty(), True)

        test1 = Section(0, 5)
        test2 = Section(5, 10)

        test.intersection(test1, test2)
        self.assertTrue(test.isempty(), False)
        self.assertTrue(test.start, 5)
        self.assertTrue(test.end, 5)

        test1 = Section(0, 6)
        test2 = Section(2, 10)
        test.intersection(test1, test2)
        self.assertTrue(test.isempty(), False)
        self.assertTrue(test.start, 2)
        self.assertTrue(test.end, 6)
