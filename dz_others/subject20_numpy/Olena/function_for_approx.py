#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
модуль з функціями для лінійної апроксимації

розв'язання системи лінійних рівнянь проводиться прямим методом LR Гаусса

# виконала: Олена Мішнева
"""

import numpy as np
import random


ITERATION_LIMIT = 1000


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


def gauss_meth(coeff_matrix: np.ndarray, free_vector: np.ndarray) -> np.ndarray:
    """
    LR метод Гаусса розв'язання СЛР  Ax = b
    :param coeff_matrix: матриця коефіцієнтів
    :param free_vector: матриця вільних членів
    :return:
    """
    upper = coeff_matrix.copy()

    # прямий хід алгоритма Гауса
    for i in range(coeff_matrix.shape[0] - 1):
        if upper[i, i] == 0:                              # перевірка, чи діагональний елемент ненульовий
            for j in range(i, coeff_matrix.shape[0]):     # якщо нульовий, то міняємо рядок з тим, де ненульовий
                if upper[j, i] != 0:
                    upper[j], upper[i] = upper[i], upper[j]   # одночасно міняємо рядки в матриці коефіцієнтів
                    free_vector[j], free_vector[i] = free_vector[i], free_vector[j]  # і в векторі вільних членів
                    break
            else:                     # якщо цикл завершився без зупинки, то ненульових елементів на
                continue              # і-му стовпчику нема

        free_vector[i] = free_vector[i] / upper[i, i]    # скорочення рядка
        upper[i] = upper[i] / upper[i, i]

        for j in range(i + 1, coeff_matrix.shape[0]):   # обнуляння елементів j-ого стовпчика, які під і-им рядком
            tmp = upper[j, i]
            upper[j] -= tmp * upper[i]
            free_vector[j] -= tmp * free_vector[i]

    # розрахунок коренів з нової слр (Ux = L^-1 * b)
    n = coeff_matrix.shape[1]
    res = np.zeros(n)
    res[-1] = free_vector[n-1] / upper[n-1, n-1]
    for i in range(n-2, -1, -1):
        for j in range(n-1, i, -1):
            free_vector[i] = free_vector[i] - upper[i, j] * res[j]
        res[i] = free_vector[i] / upper[i, i]
    return res


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
    test_a = np.array([[2., 5., 7.], [6., 3., 4.], [5., -2., -4.]])
    test_b = np.array([1., 2., 3.])

    print(np.linalg.solve(test_a, test_b))    # розв'язання слр за допомогою numpy
    print(gauss_meth(test_a, test_b))         # розв'язання методом Гаусса  (для порівняння)
