#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np
from math import sin


def gety(f, x):
    """Повертає значення функції f для всіх точок з x
    """
    try:
        y = f(x)
    except Exception as e:
        print('Exception handling', e)
        n = x.size
        y = np.zeros(n)
        for i in range(n):
            y[i] = f(x[i])
    return y


def tabulate(f, a, b, n):
    """Табулює функцію f на інтервалі [a,b] у n точках
    """
    x = np.linspace(a, b, n)
    y = gety(f, x)
    return x, y


def fun(x):
    """x**3 - 7*x - 1
    """
    return x**3 - 7*x - 1


if __name__ == '__main__':
    test_n = int(input('Кількість точок: '))
    test_a = float(input('Початок відрізку: '))
    test_b = float(input('Кінець відрізку: '))

    funcs = [fun, sin, np.vectorize(sin)]
    for ff in funcs:
        test_x, test_y = tabulate(ff, test_a, test_b, test_n)
        if test_n < 50:
            print('\n\n', test_x, '\n\n', test_y)
        print('Зроблено для', str(ff))
