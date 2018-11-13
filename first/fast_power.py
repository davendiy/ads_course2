#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


def fast_pow(x, n):

    if n == 0:
        return 1
    elif n % 2 == 0:
        return fast_pow(x * x, n // 2)
    else:
        return fast_pow(x * x, n // 2) * x
