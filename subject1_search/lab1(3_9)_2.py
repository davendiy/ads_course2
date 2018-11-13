#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def read_line(message: str, len_list: int):
    """
    функція коректоного зчитування вхідних даних
    :param message: повідомлення при зчитуванні
    :param len_list: довжина списку, який зчитується
    :return: відсортований список кортежів (ознака, початковий індекс)
    """
    s = input(message)
    s = s.split()
    s = list(map(lambda a, i: (int(a), i + 1), s, range(len_list)))
    s.sort(key=lambda a: a[0])
    return s


def find_deer(deer_list: list, first_elf: tuple, second_elf: tuple):
    """
    функція знаходження оленя за вхідними ельфами
    :param deer_list: список оленів
    :param first_elf: перший ельф (менший)
    :param second_elf: другий (більший)
    :return: олень, або None
    """
    rez = None
    for deer in deer_list:    # проходимо по всіх оленях
        # якщо олень задовольняє умову - запам'ятовуємо його
        if first_elf[0] < deer[0] < second_elf[0]:
            rez = deer
            break
        # якщо олень уже більший ніж другий ельф, то далі шукати нема сенсу
        elif deer[0] > second_elf[0]:
            break
    return rez


def check_right(count_of_deers: int, list1: list, list2: list):
    """
    функція перевірки відповіді (чи можливо відібрати таку к-ть оленів)
    :param count_of_deers: к-ть оленів
    :param list1: список оленів
    :param list2: список ельфів
    :return: bool, список вірних трійок
    """
    count = 0
    tmp_list1 = list1[:]         # тимчасова копія списку (там будуть видалятись елементи)

    # якщо ельфів достатня к-ть - перевіряємо
    if len(list2) >= count_of_deers * 2:
        for i in range(count_of_deers):
            # шукаємо підходящого оленя для і-го і N - k + і-ого ельфів
            tmp_deer = find_deer(tmp_list1, list2[i], list2[-count_of_deers + i])
            if tmp_deer is None:  # якщо не знайшли, то далі нема сенсу перевіряти
                break
            else:
                count += 1        # якщо знайшли, то видаляємо цього оленя, а к-ть трійок збільшуємо на 1
                tmp_list1.remove(tmp_deer)
    return count == count_of_deers


def binary_search(start: int, end: int, list1: list, list2: list):
    """
    бінарний пошук по відповідям
    :param start: мінімальна можлива відповідь
    :param end: максимальна можлива відповідь
    :param list1: список оленів
    :param list2: список ельфів
    :return: відповідь
    """
    while abs(start - end) > 1:
        tmp = (start + end) // 2
        if check_right(tmp, list1, list2):
            start = tmp
        else:
            end = tmp
    return end if check_right(end, list1, list2) else start


def finish(count, list1, list2):
    rez = []
    for i in range(count):
        # шукаємо підходящого оленя для і-го і N - k + і-ого ельфів
        tmp_deer = find_deer(list1, list2[i], list2[-count + i])
        list1.remove(tmp_deer)
        rez.append((tmp_deer[1], list2[i][1], list2[-count + i][1]))
    return rez


if __name__ == '__main__':
    list_length = list(map(int, input("").split()))
    array1 = read_line('', list_length[0])
    array2 = read_line('', list_length[1])
    result = binary_search(0, list_length[0], array1, array2)
    print(result)
    result = finish(result, array1, array2)
    for tmp_tuple in result:
        print("{} {} {}".format(*tmp_tuple))
