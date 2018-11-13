#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import random

K = 17

with open('input.txt', 'w') as file:

    for i in range(K ** 2):
        a = [str(random.randrange(0, 100)) for j in range(16)]
        file.write(' '.join(a) + '\n')
