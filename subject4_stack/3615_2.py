#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

with open('output.txt', 'w', encoding='utf-8') as output_file:
    with open('input.txt', 'r', encoding='utf-8') as file:
        a = []
        file.readline()
        for line in file:
            tmp = line.strip().split()
            if len(tmp) < 3:
                continue
            tmp1 = int(tmp[1])
            tmp2 = int(tmp[2])

            if tmp[0] == '+':
                a.insert(tmp1, tmp2)
            elif tmp[0] == '?':
                res = min(a[tmp1-1:tmp2])
                output_file.write("{}\n".format(res))
