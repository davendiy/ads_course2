#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 13.03.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.

GLOBAL_TEST = ''


def task2(dp, l, r):

    if dp[l][r] != -1:
        return dp[l][r]

    if '.' not in GLOBAL_TEST[l:r+1]:
        dp[l][r] = (r - l + 1) ** 0.5
        return dp[l][r]

    if 'X' not in GLOBAL_TEST[l:r+1]:
        dp[l][r] = 0
        return dp[l][r]

    res_min = (r - l + 1) ** 0.5
    for i in range(l, r):
        tmp = task2(dp, i + 1, r) + task2(dp, l, i)
        if tmp < res_min:
            res_min = tmp
    dp[l][r] = res_min
    return res_min


if __name__ == '__main__':
    file_in = open('input.txt', 'r')
    file_out = open('output.txt', 'w')
    for test in file_in:
        test = test.strip()
        GLOBAL_TEST = test
        dp = [[-1 for _ in range(len(test)+1)] for __ in range(len(test)+1)]
        file_out.write('{:.4f}\n'.format(task2(dp, 0, len(test)-1), 4))
    file_in.close()
    file_out.close()
