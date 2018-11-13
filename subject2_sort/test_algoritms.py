#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import functools
import random


def benchmark(f):
    """Декоратор @benchmark для обчислення часу виконання функції f.

    """
    import time

    @functools.wraps(f)  # декоратор оновлює значення атрибутів
    # _benchmark відповідними атрибутами f
    def _benchmark(*args, **kw):
        t = time.clock()  # вимірюємо час перед викликом функції
        rez = f(*args, **kw)  # викликаємо f
        t = time.clock() - t  # вимірюємо різницю у часі після виклику функції
        print('{0} time elapsed {1:.8f}'.format(f.__name__, t))
        return rez

    return _benchmark


@benchmark
def bubble_sort(array):
    """ Реалізує алгоритм сортування "Бульбашкою"

    :param array: Масив (список однотипових елементів)
    :return: None
    """
    n = len(array)
    t = 1
    start = 0
    for pass_num in range(n - 1, 0, -1):
        start1 = start
        count = 0
        pass_num1 = pass_num
        # print(array)
        if t < 0:
            start1, pass_num1 = pass_num1, start1
            start += 1
        for i in range(start1, pass_num1, t):
            # Якщо наступний елемент менший за попередній
            if (array[i] > array[i + t] and t > 0) or (array[i + t] > array[i] and t < 0):
                # Міняємо місцями елементи, тобто
                # виштовхуємо більший елемент нагору
                array[i], array[i + t] = array[i + t], array[i]
                count += 1
        if count == 0:
            break
        t = -t


@benchmark
def selection_sort(array):
    """ Реалізує алгоритм сортування вибором

    :param array: Масив (список однотипових елементів)
    :return: None
    """
    n = len(array)
    for i in range(n - 1, 0, -1):
        # реалізуємо пошук найбільшого елементу
        maxpos = 0
        for j in range(1, i + 1):
            if array[maxpos] < array[j]:
                maxpos = j

        # Міняємо місцями поточний і найбільший елемент
        array[i], array[maxpos] = array[maxpos], array[i]


@benchmark
def insertion_sort(array):
    """ Реалізує алгоритм сортування вставкою

    :param array: Масив (список однотипових елементів)
    :return: None
    """
    n = len(array)
    for index in range(1, n):

        current_value = array[index]
        position = index

        # пошук позиції для вставки поточного елемента
        while position > 0:
            if array[position - 1] > current_value:
                # зсув елементу масиву вправо
                array[position] = array[position - 1]
            else:
                # знайдено позицію
                break
            position -= 1

        # Вставка поточного елемента у знайдену позицію
        array[position] = current_value


@benchmark
def merge_sort_test(array):
    return merge_sort(array)


def merge_sort(array):
    """ Реалізує алгоритм сортування злиттям

    :param array: Масив (список однотипових елементів)
    :return: None
    """
    # print("Splitting ", array)
    if len(array) > 1:
        # Розбиття списку навпіл
        mid = len(array) // 2
        lefthalf = array[:mid]
        righthalf = array[mid:]

        # Рекурсивний виклик сортування
        # для кожної з половин
        merge_sort(lefthalf)
        merge_sort(righthalf)

        # Злиття двох відсортованих списків
        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                array[k] = lefthalf[i]
                i += 1
            else:
                array[k] = righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            array[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            array[k] = righthalf[j]
            j += 1
            k += 1


@benchmark
def quick_sort(array):
    """ Реалізує алгоритм швидкого сортування

    :param array: Масив (список однотипових елементів)
    :return: None
    """
    quick_sort_helper(array, 0, len(array) - 1)


def quick_sort_helper(array, first, last):
    """ Допоміжний рекурсивний метод,
        що реалізує сортування фрагменту списку обмеженого заданими позиціями

    :param array: Масив (список однотипових елементів)
    :param first: Ліва межа списку
    :param last: Права межа списку
    :return: None
    """
    if first < last:
        # Визанчення точки розбиття спику
        splitpoint = partition(array, first, last)
        # Рекурсивний виклик функції швидкого сортування
        # для отриманих частин списку
        quick_sort_helper(array, first, splitpoint - 1)
        quick_sort_helper(array, splitpoint + 1, last)


def partition(array, first, last):
    """ Визначає точку розбиття списку

    :param array: Масив (список однотипових елементів)
    :param first: Ліва межа списку
    :param last: Права межа списку
    :return: Позицію розбиття списку
    """
    pivot = array[first]
    left = first + 1
    right = last
    done = False
    while not done:
        # Рухаємося зліва на право,
        # поки не знайдемо елемент, що більший за опорний
        while left <= right and array[left] <= pivot:
            left += 1

        # Рухаємося справа на ліво,
        # поки не знайдемо елемент, що менший за опорний
        while array[right] >= pivot and right >= left:
            right -= 1

        # Якщо індекс правого елемента менший за індекс лівого
        if right < left:
            # то розбиття списку завершено
            done = True
        else:
            # міняємо знайдений елементи місцями
            array[left], array[right] = array[right], array[left]

    # ставимо опорний елемент на його позицію
    array[first], array[right] = array[right], array[first]
    return right


@benchmark
def sort_(array):
    return sorted(array)


@benchmark
def bubble_sort2(array):
    """ Реалізує алгоритм сортування "Бульбашкою"

    :param array: Масив (список однотипових елементів)
    :return: None
    """
    n = len(array)
    for pass_num in range(n - 1, 0, -1):
        for i in range(pass_num):
            # Якщо наступний елемент менший за попередній
            if array[i] > array[i + 1]:
                # Міняємо місцями елементи, тобто
                # виштовхуємо більший елемент нагору
                array[i], array[i + 1] = array[i + 1], array[i]


if __name__ == "__main__":

    functions = (bubble_sort, merge_sort_test, selection_sort, insertion_sort, quick_sort, sort_, bubble_sort2)
    test = []
    for test_num in range(5000):
        test.append(random.uniform(0, 700))

    print(test)
    for func in functions:
        print('\nfunction: {}'.format(func.__name__))
        print(func(test[:]))

    # arr = [1, 3, 7, 3, 6, 1, 3, 6, 1, 0, 8, 5, 10, 7]
    # bubble_sort(arr)
    # print(arr)
