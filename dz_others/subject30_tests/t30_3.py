#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import unittest


def hamming_distance(s1, s2):
    """ Hamming distance between s1 and s2

    >>> hamming_distance('aa', 'bb')
    2
    >>> hamming_distance('ab', 'ab')
    0
    >>> hamming_distance('ab', 'a')
    1
    >>> hamming_distance('asdasd', 'asdasda')
    1
    >>> hamming_distance('', 'b')
    1
    >>> hamming_distance('', '')
    0
    >>> hamming_distance('AA', 'aa')
    2
    >>> hamming_distance('ab', 'aB')
    1

    :param s1: string
    :param s2: string
    :return: integer
    """
    i = 0
    for a, b in zip(s1, s2):
        if a != b:
            i += 1
    i += abs(len(s1) - len(s2))
    return i


class Test(unittest.TestCase):

    def test1(self):
        self.assertEqual(hamming_distance('aa', 'aa'), 0)
        self.assertEqual(hamming_distance('qwerty', 'qwerty'), 0)
        self.assertEqual(hamming_distance('lsadfjalsdkfj lsdkjfs sd', 'lsadfjalsdkfj lsdkjfs sd'), 0)

    def test2(self):
        self.assertEqual(hamming_distance('aaaaaBBB', 'aaaaa'), 3)
        self.assertEqual(hamming_distance('aaaaBBBB', 'BBBB'), 4)
        self.assertEqual(hamming_distance('', 'abs'), 3)

    def test3(self):
        self.assertEqual(hamming_distance('', ''), 0)
        self.assertEqual(hamming_distance('ASD', 'asd'), 0)
