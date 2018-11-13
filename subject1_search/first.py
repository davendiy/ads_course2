#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def find_all2(array):

    bins = [1]
    rez = []
    for i in array:
        while i < bins[-1]:
            bins.append(bins[-1] << 1)
        if i in bins:
            rez.append(i)
    return rez


def bin_search(lst, x):
    n = len(lst) - 1
    m = n // 2
    if n <= 0:
        return lst[0] == x if n == 0 else False

    else:
        return bin_search(lst[0:m], x) if x <= lst[m] else bin_search(lst[m:n], x)


def bin_search2(lst, x, a, b):
    m = (a + b) // 2

    if b - a <= 1:
        return lst[a] == x if b - a == 1 else False

    else:
        return bin_search2(lst, x, a, m) if lst[m] >= x else bin_search2(lst, x, m, b)


if __name__ == '__main__':
    test = [2, 3, 4, 5, 6, 7, 8, 9, 34, 52, 1024]
    print(bin_search(test, 52))
    print(bin_search2(test, 52, 0, len(test)))
