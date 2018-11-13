#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import random

K = 22

with open('input.txt', 'w') as file:

    for i in range(K ** 2):
        a = [str(random.randrange(0, 100)) for j in range(16)]
        file.write(' '.join(a) + '\n')
