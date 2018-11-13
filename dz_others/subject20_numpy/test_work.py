#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import numpy as np
from math import sqrt
import matplotlib.pyplot as plt


K = 3
G = 1

R = [K + i for i in range(-2, 3)]

ITERATION_LIMIT = 1000
START_Y = 1


# стилі ліній
styles = ['-', '--', '-.', ':', '.', ',',
          'o', 'v', '^', '<', '>',
          '1', '2', '3', '4',
          's', 'p', '*', 'h', 'H',
          '+', 'x', 'D', 'd', '|', '_']

# кольори ліній
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


number_of_style = 0


def f(x):
    return -x ** 4 + 2 * x ** 2


def gety(func, x):
    """Повертає значення функції f для всіх точок з x
    """
    try:
        y = func(x)
    except Exception as e:
        print('Exception handling', e)
        n = x.size
        y = np.zeros(n)
        for i in range(n):
            y[i] = func(x[i])
    return y


def tabulate(func, start, end, n, r):
    """Табулює функцію f на інтервалі [a,b] у n точках
    """
    x = np.linspace(start, end, n)
    x = x * r
    y = gety(func, x)
    return x, y


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


def plot(x, y, string):
    global number_of_style

    plt.xlabel('x')
    plt.ylabel('y')
    style = styles[number_of_style % len(styles)] + colors[number_of_style % len(colors)]
    number_of_style += 1
    plt.plot(x, y, style, label=string)
    plt.legend(loc='best')


def read_matrix(filename):
    """
    зчитування матриці з текстового файлу
    """
    matrix = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            tmp = list(map(int, line.split()))
            matrix.append(tmp)
    return np.matrix(matrix)


def overdiag(matrix: np.matrix, pos=1):
    """
    функція, яка відділяє з матриці наддіагональ або піддіагональ
    """
    result = []
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):

            if j - i == pos:
                result.append(matrix[i, j])
    return np.array(result)


def norm(vector):
    """
    функція знаходження норми вектора (варіант 3)
    """
    return sqrt(sum(vector ** 2))


def sum1(vector):
    """
    функція знаходження суми всіх елементів вектора
    """
    res = 0
    for i in range(vector.shape[1]):
        res += vector[0, i]
    return res


def eigen(matx: np.matrix, eps=1e-3):
    """
    функція знаходження власного числа і вектора методом скалярних добутків
    """
    tr_matrix = matx.transpose()
    y = np.zeros(matx.shape[0])
    z = np.zeros(matx.shape[0])
    y[0] = START_Y
    z[0] = y[0]
    eigenvalue = 0
    for j in range(ITERATION_LIMIT):
        if y.shape[0] == 1:
            y = y.transpose()
        if z.shape[0] == 1:
            z = z.transpose()
        next_y = np.array(matx.dot(y))
        next_z = np.array(tr_matrix.dot(z))

        tmp1 = sum1(next_y * next_z)
        tmp2 = sum1(y * next_z)

        tmp_res = tmp1 / tmp2
        if j == 0:
            eigenvalue = tmp_res
        elif abs(eigenvalue - tmp_res) < eps:
            break
        else:
            eigenvalue = tmp_res
        y = next_y
        z = next_z

    eigenvector = y / norm(y)
    return eigenvalue, eigenvector


for tmp_r in R:
    arr_x, arr_y = tabulate(f, -10, 10, 56, tmp_r)
    movespinesticks()
    plot(arr_x, arr_y, 'f(x * {})'.format(tmp_r))
    plt.show()

B = read_matrix('input.txt')

print('матриця B:\n', B)

A = B.reshape((4 * K, 4 * K))
print("матриця A:\n", A)

a = overdiag(A, -1)
b = overdiag(A, 1)
print("піддіагональ:\n", a, '\nнаддіагональ:\n', b)

d = a * b
d = d.sum()

np.fill_diagonal(A, d * A.diagonal())
print("змінена матриця:\n", A)


eigval, eigvec = eigen(A)
print('власний вектор:\n', eigvec, 'власне число:', eigval)

print(norm(A.dot(eigvec) - eigval * eigvec))
