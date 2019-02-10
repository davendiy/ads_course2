#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com
import random
import time

n = 100


with open('input.txt', 'w') as file:

    pars = ["(", "]", ')']
    j = 0
    res_str = '(' * 5
    for i in range(3, n):
        numb = random.randrange(5)
        numb = 0 if numb in [3, 4] else numb
        res_str += pars[numb]
        if i % 72 == 0:
            res_str += '\n'

    file.write('{} {}\n'.format(n+1, res_str.count(']') + 1))
    file.write(res_str + ']')
    print(len(res_str + ']'))

print('waiting for second program...')
while True:
    try:
        with open('output.txt', 'r') as file:
            msg = file.readlines()
    except IOError:
        continue
    if msg:
        with open('output.txt', 'w'):
            pass
        break
    time.sleep(1)
print(msg)
numbers = list(map(int, msg))

with open('input.txt', 'r') as file:
    tmp = file.readline()
    string = file.read()

print(string)

if numbers[0] == 0:
    print(0)
    exit(0)

j = 1
rez_str = ''
succ = 0
succ2 = True
for par in string:
    if par == ']':
        for i in range(numbers[j]):
            rez_str += ')'
            succ -= 1
        j += 1
    elif par == '(':
        succ += 1
        rez_str += par
    else:
        succ -= 1
        rez_str += par
    if succ < 0:
        succ2 = False

succ = succ2 and succ == 0
print(rez_str)
print(succ)
