#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np
from math import sqrt
from numpy import sign


ITERATION_LIMIT = 10000


def _sds_decomposition(a: np.array):
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
    # print(tmp_s, '\n', tmp_d)
    return tmp_s, tmp_d


def square_method(a: np.array, b: np.array):
    """
    розв'язує симетричну слр методом квадратного кореня
    :param a: матриця коефіцієнтів
    :param b: матриця вільних членів
    :return: матриця невідомих
    """
    tmp_s, tmp_d = _sds_decomposition(a)    # розклад симетричної матриці
    tmp_s_t = tmp_s.transpose()             # транспонування
    n = a.shape[0]
    y = np.zeros(n)                               # створення допоміжної матриці з проміжними невідомими
    y[0] = b[0] / (tmp_s[0, 0] * tmp_d[0, 0])     # заповнення матриці проміжних невідомих
    for i in range(1, n):
        y[i] = (b[i] - sum(tmp_d[l, l] * y[l] * tmp_s_t[l, i] for l in range(i))) / \
               (tmp_s[i, i] * tmp_d[i, i])

    x = np.zeros(n)     # заповнення матриці кінцевих невідомих
    x[n-1] = y[n-1] / tmp_s[n-1, n-1]
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - sum(tmp_s[l, i] * x[l] for l in range(i + 1, n))) / (tmp_s[i, i])

    return x


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


def simple_iteration(a: np.array, b: np.array, t: float, eps=10e-10):
    """
    метод простої ітерації з параметром
    :param a: матриця коефіцієнтів
    :param b: матриця вільних членів
    :param t: параметр
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


def min_mismatch(a: np.array, b: np.array, eps=10e-9):
    """
    розв'язування системи лінійних рівнянь методом мінімальних нев'язок
    :param a: матриця коефіцієнтів
    :param b: вектор вільних членів
    :param eps: точність
    :return: вектор коренів
    """
    tmp_x = np.zeros_like(b) + 1    # вибираємо будь-яке x_0

    # ітерації
    for i in range(ITERATION_LIMIT):
        pre_x = tmp_x                 # х_к-1
        r_k = a.dot(tmp_x) - b        # нев'язка
        # параметр, який залежить від нев'язки
        tau_k = np.sum(a.dot(r_k) * r_k) / np.sum(a.dot(r_k) ** 2)
        tmp_x = tmp_x - tau_k * r_k          # х на к-тій ітерації
        if np.sum(np.abs(tmp_x - pre_x)) < eps:    # додаткова умова виходу
            break
    return tmp_x


def fastest_descent(a: np.array, b: np.array, eps=10e-9):
    """
    розв'язування слр методом швидкого спуску
    :param a: матриця коефіцієнтів
    :param b: вектор вільних членів
    :param eps: похибка
    :return: вектор коренів
    """
    tmp_x = np.zeros_like(b) + 1

    for i in range(ITERATION_LIMIT):
        pre_x = tmp_x
        r_k = a.dot(tmp_x) - b
        tau_k = np.sum(r_k * r_k) / np.sum(a.dot(r_k) * r_k)
        tmp_x = tmp_x - tau_k * r_k
        if np.sum(np.abs(tmp_x - pre_x)) < eps:
            break
    return tmp_x


if __name__ == '__main__':

    test_a = np.array([[100., 1., 3.],
                       [1., 200., 2.],
                       [3., 2., 800.]])

    test_b = np.array([0., 2., 2.])

    tau = 0.00015

    result1 = simple_iteration(test_a, test_b, tau)
    print(result1, '\n')

    result2 = jacobi(test_a, test_b)
    print("jacobi")
    print(result2, '\n')

    result3 = square_method(test_a, test_b)
    print('\nsquare')
    print(result3)

    result4 = min_mismatch(test_a, test_b)
    print('\nmistmatch')
    print(result4)

    result5 = fastest_descent(test_a, test_b)
    print('\nfastest')
    print(result5)
