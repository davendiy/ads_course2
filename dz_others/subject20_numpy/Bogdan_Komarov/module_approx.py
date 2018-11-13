#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
модуль з функціями для лінійної апроксимації

розв'язання системи лінійних рівнянь проводиться методом квадратного кореня
"""

import numpy as np
import random
from numpy import sign
from math import sqrt


def print_system(a, b):
    """
    Виводить на екран систему рівнянь.

    :param a: numpy 2-вимірний масив коефіцієнтів
    :param b: numpy масив вільних членів
    """
    print("Система:")
    for i in range(a.shape[0]):

        # a.shape[0] - кількість рядків, a.shape[1] - кількість стовпчиків матриці
        row = ["{}*x{}".format(a[i, j], j + 1) for j in range(a.shape[1])]
        print(" + ".join(row), " = ", b[i])
    print()


def tabulate_with_fault(func, a: float, b: float, n: int, eps: float):
    """
    процедура табулювання функції з похибкою

    :param func: функція
    :param a: ліва межа відрізку
    :param b: права межа відрізку
    :param n: к-ть точок
    :param eps: похибка фізичного експерименту
    :return: x - масив numpy точок
             y - масив numpy значень функції

    """
    x = np.linspace(a, b, n)
    eta = 1
    while eta == 1:
        eta = random.uniform(0, 1)

    try:
        y = func(x) + eta * eps
    except Exception as e:
        print("exception:", e)
        y = np.zeros(n)
        for i in range(n):
            y[i] = func(x[i]) + eta * eps
    return x, y


def linear_eq_system(x: np.ndarray, y: np.ndarray, n1: int, eps: float):
    """
    створення системи лінійних рівнянь для апроксимації методом найменших квадратів
    :param x: numpy масив точок функції
    :param y: numpy масив значень функції в точках x
    :param n1: к-ть ітерацій
    :param eps:
    :return:
    """
    a = np.zeros((n1, n1))    # матриця коефіцієнтів
    b = np.zeros(n1)          # матриця вільних членів
    p = eps ** (-2)
    n2 = x.size
    for m in range(n1):
        for i in range(n2):               # реалізація формули (2)
            b[m] += p * y[i] * x[i] ** m

        for j in range(n1):
            for i in range(n2):
                a[m, j] += p * x[i] ** (j + m)
    return a, b


def _sds_decomposition(a: np.matrix):
    """
    функція, яка розкладає матрицю А на добуток матриць S^T * D * S
    :param a: матриця numpy
    :return: tmp_s - матриця numpy (S)
             tmp_d - матриця numpy (D)
    """
    tmp_s = np.matrix(np.zeros(a.shape))     # створення матриць з нулями
    tmp_d = np.matrix(np.zeros(a.shape))

    for k in range(a.shape[0]):   # поелементне знаходження всіх елементів

        tmp_sum = 0
        for i in range(k):       # проміжний результат для формул
            tmp_sum += tmp_d[i, i] * abs(tmp_s[i, k]) ** 2

        tmp_res = a[k, k] - tmp_sum
        tmp_d[k, k] = sign(tmp_res)          # діагональний елемент матриці D
        tmp_s[k, k] = sqrt(abs(tmp_res))     # діагональний елемент матриці S

        for l in range(a.shape[0]):          # заповнення інших елементів у рядку (верхньотрикутних)
            if k + 1 <= l:
                tmp_sum = sum(tmp_d[i, i] * tmp_s.transpose()[i, k] * tmp_s[i, l] for i in range(k))
                tmp_s[k, l] = (a[k, l] - tmp_sum) / (tmp_s[k, k] * tmp_d[k, k])
    print(tmp_s, '\n', tmp_d)
    return tmp_s, tmp_d


def square_method(a: np.matrix, b: np.ndarray):
    """
    розв'язує симетричну слр методом квадратного кореня
    :param a: матриця коефіцієнтів
    :param b: матриця вільних членів
    :return: матриця невідомих
    """
    tmp_s, tmp_d = _sds_decomposition(a)    # розклад симетричної матриці
    tmp_s_t = tmp_s.transpose()             # транспонування
    n = a.shape[0]

    y = np.zeros(n)            # створення допоміжної матриці з проміжними невідомими

    y[0] = b[0] / (tmp_s[0, 0] * tmp_d[0, 0])     # заповнення матриці проміжних невідомих
    for i in range(1, n):
        y[i] = (b[i] - sum(tmp_d[l, l] * y[l] * tmp_s_t[l, i] for l in range(i))) / \
               (tmp_s[i, i] * tmp_d[i, i])

    x = np.zeros(n)     # заповнення матриці кінцевих невідомих
    x[n-1] = y[n-1] / tmp_s[n-1, n-1]
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(tmp_s[l, i] * x[l] for l in range(i + 1, n))) / (tmp_s[i, i])

    return x


def result_func(coeff, x, n):
    """
    рахує значення апроксимативної функції в точках
    :param coeff: масив коефіцієнтів (корені слр)
    :param x: масив точок
    :param n: к-ть точок
    :return: масив значень
    """
    res = sum(coeff[i] * x ** i for i in range(n))
    return res


if __name__ == '__main__':

    test_a = np.matrix([[1, 2, 3], [2, 1, 2], [3, 2, 1]])
    test_b = np.array([0, 3, 2])
    result = square_method(test_a, test_b)

    print(result)
