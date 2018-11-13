#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import re


with open('input.txt', 'r') as file:
    data = file.read()

grnp = r'[\d\s] + grn|[\d\s] + grn'
usdp = r'$[\d\s] + '
grn = re.findall(data, grnp)

usd = re.findall(data, usdp)

res1 = 0
for text in grn:
    res1 += int(text[:text.index('grn')])


res2 = 0
for text in usd:
    res2 += int(text[:text.index('grn')])

