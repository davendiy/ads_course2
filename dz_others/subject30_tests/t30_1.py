#!/usr/bin/env python3
# -*-encoding: utf-8-*-


def logarithm(x, eps=10e-5):
    """ Calculate log(x + 1), |x| < 1

    >>> from math import log

    >>> abs(logarithm(0.6) - log(1.6)) < 10e-5
    True
    >>> abs(logarithm(0.8) - log(1.8)) < 10e-5
    True
    >>> abs(logarithm(0.1) - log(1.1)) < 10e-5
    True
    >>> abs(logarithm(0.3) - log(1.3)) < 10e-5
    True

    >>> logarithm(2)
    nan
    >>> logarithm(-2.5)
    nan
    >>> logarithm(1.1)
    nan

    >>> abs(logarithm(0.2, 10e-6) - log(1.2)) < 10e-6
    True
    >>> abs(logarithm(0.2, 10e-2) - log(1.2)) < 10e-2
    True
    >>> abs(logarithm(0.2, 10e-4) - log(1.2)) < 10e-4
    True

    :param x: float number
    :param eps: accurany of calculation
    :return: float number
    """
    if abs(x) >= 1:
        return float('Nan')

    pre_x = x
    tmp = x ** 2
    sign = -1
    i = 2
    res_x = pre_x + sign * tmp / i

    while abs(res_x - pre_x) > eps:
        sign = -sign
        i += 1
        tmp *= x
        pre_x = res_x
        res_x += sign * tmp / i

    return res_x
