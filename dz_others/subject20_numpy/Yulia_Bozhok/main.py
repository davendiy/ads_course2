#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
основна програма, реалізує лінійну апроксимацію функції exp(-1 / |x|), будує відповідні графіки
і виводить масиви значень в outstr20.txt

виконала: Божок Юлія
"""

from Yulia_Bozhok.function_for_approx import *
from Yulia_Bozhok.functions_for_plot import *
import math

N = 53
eps = 1e-5

# розміщення осей координат
movespinesticks()


def f(x: float):
    """
    функція завдання
    :param x: дійсне число
    :return: дійсне число
    """
    return math.e ** (-1 / abs(x)) if x != 0 else 0


# табуляція з похибкою
test_x, test_y = tabulate_with_fault(f, -1, 1, 53, 10 ** (-5))
result_x = []

# побудова графіка функції
plt.subplot(5, 1, 1)
norm_plot(test_x, test_y, 'f(x)')

# запис у файл
with open('outstr20.txt', 'w', encoding='utf-8') as file:
    file.write('сітка:')
    file.write('\n' + str(test_x))
    file.write('\n\nзначення з похибкою:')
    file.write('\n' + str(test_y))

    # лінійна апроксимація для n = 3,.. 6
    for n in range(3, 7):

        # створення системи лінійних рівнянь для апроксимації
        test_a, test_b = linear_eq_system(test_x, test_y, n, eps)

        # розв'язання слр методом якобі
        result_matrix = jacobi(test_a, test_b)

        # виведення системи рівнянь
        # print()
        # print_system(test_a, test_b)

        # відновлення значень функції
        tmp_result = result_func(result_matrix, test_x, n)

        # виведення у файл
        file.write("\n\nphi({}, x):".format(n))
        file.write('\n' + str(tmp_result))

        # побудова графіка
        plt.subplot(5, 1, n - 1)
        norm_plot(test_x, tmp_result, 'phi({}, x)'.format(n))

plt.show()
