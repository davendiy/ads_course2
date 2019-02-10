#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 06.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import sys

m = int(sys.argv[1])

a = [[float(input('a[{}, {}] = '.format(i, j))) for i in range(m)] for j in range(m)]

trace = 0
for i in range(m):
    trace += a[i][i]

print('trace =', trace)
