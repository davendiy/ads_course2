#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
модуль з додатковими функціями
"""

import numpy as np
import random
import matplotlib.pyplot as plt


ITERATION_LIMIT = 1000      # максимальна к-ть ітерацій (якщо ітераційний процес не сходиться

# стилі ліній
styles = ['-', '--', '-.', ':', '.', ',',
          'o', 'v', '^', '<', '>',
          '1', '2', '3', '4',
          's', 'p', '*', 'h', 'H',
          '+', 'x', 'D', 'd', '|', '_']

# кольори ліній
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

number_of_style = 0


# %% функції для розв'язування слр
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


def bad_tabulate(func, a: float, b: float, n: int, eps: float):
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


def create_system(x: np.ndarray, y: np.ndarray, n1: int, eps: float):
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


def simple_iteration(a: np.array, b: np.array, t=0.00001, eps=10e-10):
    """
    метод простої ітерації з параметром
    :param a: матриця коефіцієнтів
    :param b: матриця вільних членів
    :param t: параметр, підібраний методом великого математика Підбора
    :param eps: точність
    :return: вектор коренів
    """
    tmp_x = np.zeros_like(b) - 1          # вибираємо будь-яке x_0
    for i in range(ITERATION_LIMIT):      # ітерації
        pre_x = tmp_x                     # копіюємо х к-1 ітерації
        r_k = a.dot(tmp_x) - b
        tmp_x = tmp_x - t * r_k
        if np.sum(np.abs(tmp_x - pre_x)) < eps:    # додаткова умова виходу
            break
    return tmp_x


def y_from_roots(coeff, x, n):
    """
    рахує значення апроксимативної функції в точках
    :param coeff: масив коефіцієнтів (корені слр)
    :param x: масив точок
    :param n: к-ть точок
    :return: масив значень
    """
    res = sum(coeff[i] * x ** i for i in range(n))
    return res


# %% функції для побудови графіків
def movespinesticks():
    """
    Перемістити осі у нульову позицію
    """
    ax = plt.gca()  # отримати поточний об'єкт класу axes

    # зробити праву та верхню осі невидимими:
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # перенести нижню вісь у позицію y=0:
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))

    # перенести ліву вісь у позицію x == 0:
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))


def my_plot(x, y, label):
    """
    побудова графіка
    :param x: значення x
    :param y: значення у
    :param label: мітка
    """
    global number_of_style     # параметр, за допомогою якого змінюється стиль лінії і колір

    plt.xlabel('x')        # мітка осі абсцис
    plt.ylabel('y')        # мітка осі ординат

    # розрахунок номеру стиля і кольору
    style = styles[number_of_style % len(styles)] + colors[number_of_style % len(colors)]
    number_of_style += 1
    plt.plot(x, y, style, label=label)
    plt.legend(loc='best')
