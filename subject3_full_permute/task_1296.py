#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def find_max(str_number: str, count: int):

    max_prod = 0
    if count == 0:
        return int(str_number)

    if len(str_number) < count:
        return 0

    for i in range(1, len(str_number)):

        tmp1 = int(str_number[:i])
        tmp2 = find_max(str_number[i:], count-1)

        tmp_max = tmp1 * tmp2
        if tmp_max > max_prod:
            max_prod = tmp_max

    return max_prod


if __name__ == '__main__':
    res_list = []
    with open('input.txt', 'r') as file:
        for line in file:
            tmp_input = line.split()
            result = find_max(tmp_input[0], int(tmp_input[1]) - 1)
            res_list.append(result)

    with open('output.txt', 'w') as file:
        for res in res_list:
            file.write(str(res) + "\n")
