#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

with open('input.txt', 'r') as file:
    res = []
    success_balance = 1
    par_count = 0
    end_index = 0
    head = file.readline().split()
    n, m = int(head[0]), int(head[1])
    end = False
    count_end = 0
    i = -1
    tmp_symb = ' '
    while tmp_symb != '':
        i += 1
        tmp_symb = file.read(1)
        while tmp_symb == '\n':
            tmp_symb = file.readline()
            tmp_symb = file.read(1)

        if end:
            if tmp_symb == ')':
                count_end += 1
            elif tmp_symb == ']':
                success_balance = 0
                break
            continue

        if tmp_symb == '(':
            par_count += 1
        elif tmp_symb == ')' and par_count > 0:
            par_count -= 1
        elif tmp_symb == ']' and par_count > 0 and end_index < m - 1:
            res.append(1)
            end_index += 1
            par_count -= 1
        elif tmp_symb == ']' and par_count > 0 and end_index == m - 1:
            end = True
        else:
            success_balance = 0
            break
        if par_count < 0:
            success_balance = 0
            break
    if end:
        res.append(par_count - count_end)

with open('output.txt', 'w') as file:
    file.write(str(success_balance) + '\n')
    if success_balance == 1:
        for el in res:
            file.write(str(el) + '\n')
