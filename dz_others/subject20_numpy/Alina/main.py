#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
основна програма

слр розв'язується методом простої ітерації
"""

from Alina.functions import *

# к-ть елементів у сітці і точність
N = 65
eps = 1e-1

# межі функції
start = -1
end = 1.5


def f(x: float):
    """
    функція завдання
    :param x: дійсне число
    :return: дійсне число
    """
    return (1 + x) / (1 + 0.5 * x ** 3)


def write(output, label, arr: np.array):
    """
    виведення у файл великого масиву по 5 елементів в рядку
    :param output: тип-файл
    :param label: мітка
    :param arr: масив
    """
    output.write("\n# {}\n".format(label))
    np.savetxt(file, arr.reshape(N // 5, 5), fmt='%14.6E')


# табуляція з похибкою
tab_x, mistake_y = bad_tabulate(f, start, end, N, 10 ** (-5))

# побудова графіка функції
movespinesticks()
my_plot(tab_x, mistake_y, 'f(x)')
plt.show()

# запис у файл
with open('outstr20.txt', 'w', encoding='utf-8') as file:
    write(file, 'cітка', tab_x)
    write(file, 'значення з похибкою', mistake_y)

    # лінійна апроксимація для n = 3,.. 6
    for n in range(3, 7):

        # створення системи лінійних рівнянь для апроксимації
        test_a, test_b = create_system(tab_x, mistake_y, n, eps)

        # розв'язання слр методом простої ітерації
        roots = simple_iteration(test_a, test_b)

        # виведення системи рівнянь
        print()
        print_system(test_a, test_b)

        # відновлення значень функції
        tmp_y = y_from_roots(roots, tab_x, n)

        # виведення у файл
        write(file, 'phi({}, x)'.format(n), tmp_y)

        # побудова графіка
        movespinesticks()
        my_plot(tab_x, tmp_y, 'phi({}, x)'.format(n))
        plt.show()
