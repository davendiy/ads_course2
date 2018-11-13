#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from math import ceil


def binary_search(start, end, v_max: int, d: int, dandelions: list) -> int:
    tmp_time = (start + end) / 2
    while abs(start - end) > 0.1:
        poss_time, count = find_possible_time(tmp_time, v_max, d, dandelions)
        if poss_time > dandelions[-1][1]:
            end = tmp_time
        elif poss_time < dandelions[-1][1]:
            start = tmp_time
        else:
            start = tmp_time
            break
        tmp_time = (start + end) / 2
    poss_time, count = find_possible_time(start, v_max, d, dandelions)
    poss_time += d + count * d + max_dist / v_max

    return poss_time


def find_possible_time(wait: int, v_max: int, d: int, dandelions: list) -> tuple:
    time = wait
    count_behind = 0
    for dand in dandelions:
        time += dand[0] / v_max
        if time >= dand[1]:
            time += d
        else:
            count_behind += 1
    return time, count_behind


def task_read():
    v_max, d = tuple(map(int, input().split()))
    n = int(input())
    dandelions = []
    pre = 0
    max_distance = 0
    max_time = 0
    for i in range(n):
        tmp = input().split()
        tmp_distance, tmp_time = int(tmp[0]), tmp[1]
        tmp_distance, pre = tmp_distance - pre, tmp_distance
        tmp_time = tmp_time.split(':')
        tmp_time = int(tmp_time[0]) * 60 + int(tmp_time[1])
        dandelions.append((tmp_distance, tmp_time))
        if i == n - 1:
            max_distance = pre
            max_time = tmp_time
    return v_max, d, dandelions, max_distance, max_time


if __name__ == '__main__':
    test_v, test_d, test_dand, max_dist, last_time = task_read()
    result = binary_search(0, last_time, test_v, test_d, test_dand)
    result = ceil(result)
    result_h = str((result // 60) % 24)
    result_m = str(result % 60)
    result_h = '0' * (2 - len(result_h)) + result_h
    result_m = '0' * (2 - len(result_m)) + result_m
    result = '{}:{}'.format(result_h, result_m)
    print(result)
