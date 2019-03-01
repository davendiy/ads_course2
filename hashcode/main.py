#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 28.02.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np


def input_data(name_list) -> np.ndarray:
    """
    возвращает список кортежей тегов [( (index), "V", "red"), ( (index), "H", "blue")]
    :param name_list: список имен файлов
    :return:
    """
    data = []
    for file in name_list:
        with open(file, 'r') as f:
            index = 0
            for line in f.readlines()[1:]:
                data.append(((index, ), *tuple(line.split())))
                index += 1
    return np.array(data)


def read(filename):

    horizontal = []
    vertical = []
    with open(filename, 'r') as file:
        for line in file:

            tags = set(line.split()[2:])

            if line[0] == 'H':
                horizontal.append(tags)
            elif line[0] == 'V':
                vertical.append(tags)
    return horizontal, vertical


def prepare_pairs(vertical):
    res = []
    for i, el1 in enumerate(vertical):
        row = []
        for j, el2 in enumerate(vertical):
            row.append(el1.union(el2))
        res.append(row)
    return res


def score(tags1: set, tags2: set):
    return min(len(tags1.intersection(tags2)), len(tags1.difference(tags2)), len(tags2.difference(tags1)))


def algorithm(horizontal, vertical):
    used = set()
    pairs = prepare_pairs(vertical)

    n = len(vertical)

    dp = [horizontal[0]]
    dp_indexes = [0]
    now_score = 0
    for i in range(len(horizontal) + len(vertical)):
        print(i)
        if len(dp) == 1:
            max_score = 0
            max_index = (0, )
            max_el = 0
            for j, el in enumerate(horizontal):
                tmp_score = score(el, dp[0])
                if tmp_score > max_score:
                    max_score = tmp_score
                    max_index = (j, )
                    max_el = el
            for j in range(n):
                for k in range(n):
                    tmp_score = score(dp[0], pairs[j][k])
                    if tmp_score > max_score:
                        max_index = (j, k)
                        max_score = tmp_score
                        max_el = pairs[j][k]

            dp.append(max_el)
            dp_indexes.append(max_index)
            if len(max_index) == 2:
                used.add(max_index[0])
                used.add(max_index[1])
        else:
            best_place = 0
            max_score = now_score
            max_index = (0, )
            max_el = 0

            for j in range(i):
                tmp_score = now_score
                if 0 < j < i:
                    tmp_score -= score(dp[j-1], dp[j])
                for k, el in enumerate(horizontal):
                    tmp_tmp_score = tmp_score
                    if j > 0:
                        tmp_tmp_score += score(el, dp[j-1])
                    if j < i:
                        tmp_tmp_score += score(el, dp[j])
                    if tmp_tmp_score > max_score:
                        max_score = tmp_tmp_score
                        max_index = (k, )
                        max_el = el
                        best_place = j
                for k in range(n):
                    if k in used:
                        continue
                    for k2 in range(n):        # TODO доробити заміну
                        if k2 in used:
                            continue
                        tmp_tmp_score = tmp_score
                        if j > 0:
                            tmp_tmp_score += score(dp[j-1], pairs[k][k2])
                        if j < i:
                            tmp_tmp_score += score(dp[j], pairs[k][k2])
                        if tmp_tmp_score > max_score:
                            max_score = tmp_tmp_score
                            max_index = (k, k2)
                            max_el = pairs[k][k2]
                            best_place = j
            dp.insert(best_place, max_el)
            dp_indexes.insert(best_place, max_index)
            if len(max_index) == 2:
                used.add(max_index[0])
                used.add(max_index[1])
    return dp


if __name__ == '__main__':
    test_horisontal, test_vertical = read('c_memorable_moments.txt')
    tmp_res = algorithm(test_horisontal, test_vertical)
    res_score = 0
    for i in range(1, len(tmp_res)):
        res_score += score(tmp_res[i-1], tmp_res[i])
    print(res_score)
    print(tmp_res)
