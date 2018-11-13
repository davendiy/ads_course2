#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
основна програма

слр розв'язується методом швидкого спуску
"""

from Yulia_Stepanova.module import *
import math

# к-ть елементів у сітці і точність
N = 55
eps = 1e-3

# межі функції
start = -1
end = 1.5

# розміщення осей координат
movespinesticks()


def f(x: float):
    """
    функція завдання
    :param x: дійсне число
    :return: дійсне число
    """
    return math.sinh(0.5 * x) - 1


def write_file(outfile, label, array: np.array):
    """
    виведення у файл великого масиву по 5 елементів в рядку
    :param outfile: тип-файл
    :param label: мітка
    :param array: масив
    """
    outfile.write("\n# {}\n".format(label))
    np.savetxt(file, array.reshape(N // 5, 5), fmt='%14.6E')


# табуляція з похибкою
tab_x, mistake_y = task_tabulate(f, start, end, N, eps)
result_x = []

# побудова графіка функції
plot(tab_x, mistake_y, 'f(x)')
plt.show()

# запис у файл
with open('outstr20.txt', 'w', encoding='utf-8') as file:
    write_file(file, 'cітка', tab_x)
    write_file(file, 'значення з похибкою', mistake_y)

    # лінійна апроксимація для n = 3,.. 6
    for n in range(3, 7):

        # створення системи лінійних рівнянь для апроксимації
        test_a, test_b = create_system(tab_x, mistake_y, n, eps)

        # розв'язання слр методом швидкого спуску
        roots = fastest_descent(test_a, test_b)

        # виведення системи рівнянь
        print()
        print_system(test_a, test_b)

        # відновлення значень функції
        tmp_result = create_y(roots, tab_x, n)

        # виведення у файл
        write_file(file, 'phi({}, x)'.format(n), tmp_result)

        # побудова графіка
        movespinesticks()
        plot(tab_x, tmp_result, 'phi({}, x)'.format(n))
        plt.show()
