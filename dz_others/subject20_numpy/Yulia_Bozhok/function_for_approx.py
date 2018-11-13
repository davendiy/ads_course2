#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
модуль з функціями для лінійної апроксимації

розв'язання системи лінійних рівнянь проводиться методом Якобі

# виконала: Божок Юлія
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


def check_convergence(a: np.ndarray):
    """
    Перевіряє, чи сходиться
    ітераційний процес для системи рівнянь з матрицею a.

    :param a: numpy 2-вимірний масив, або numpy матриця
    :return: bool
    """
    d = np.diag(a)  # діагональні елементи a
    dd = np.abs(d) * 2  # подвоєні модулі діагональних елементів a
    na = np.sum(np.abs(a), axis=1)  # суми модулів елементів рядків матриці a
    return np.all(dd >= na) and np.any(dd > na)


def jacobi(a, b, eps=1.0e-10):
    """
    Розв'язання слр ах = b методом Якобі

    :param a: numpy 2-вимірний масив, або numpy матриця
    :param b: numpy масив
    :param eps: точність
    :return: numpy масив - корені
    """
    # if not check_convergence(a):
    #     raise ValueError("Не сходиться ітераційний процес")

    c = a.copy()
    d = np.diag(a)  # діагональні елементи a
    np.fill_diagonal(c, 0.0)  # заповнюємо діагональні елементи c нулями
    c /= d[:, np.newaxis]     # ділимо всі елементи c на діагональні елементи a

    # ділення повинно відбуватись по рядках, а саме кожен елемент i-го рядку
    # матриці c треба ділити на i-й елемент d
    # для правильного поширення треба вектор d розглядати як вектор-стовпчик
    # або матрицю з 1 стовпчиком, що робиться за допомогою d[:,np.newaxis]
    g = b / d  # ділимо всі елементи b на діагональні елементи a

    x = g.copy()  # початкове наближення
    for it_count in range(ITERATION_LIMIT):
        # print("Current solution:", x)
        x_new = g - np.dot(c, x)  # обчислюємо нове наближення
        if np.sum(np.abs(x - x_new)) < eps:  # перевірка на "близькість" x, x_new
            break
        x = x_new

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
