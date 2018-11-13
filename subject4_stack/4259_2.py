#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

file = open('input.txt', 'r')
out_file = open('output.txt', 'w')
test = []
t = True
tmp_min = None
for line in file:
    if t:
        t = False
        continue
    tmp = list(map(int, line.split()))
    if tmp[0] == 1:
        if tmp_min is None:
            tmp_min = tmp[1]
        elif tmp[1] < tmp_min:
            tmp_min = tmp[1]
        test.append(tmp[1])
    elif tmp[0] == 2:
        a = test.pop()
        if a == tmp_min and test:
            tmp_min = min(test)
        elif a == tmp_min:
            tmp_min = None
    else:
        out_file.write(str(tmp_min) + '\n')
file.close()
out_file.close()
