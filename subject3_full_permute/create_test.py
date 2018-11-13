#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import itertools
from string import ascii_lowercase
import random

LIST_WORDS = list(set('hello idi why david hi jane dick dictionary away go naher starkon pozhalusta ' 
                      'serious batman superman lost found read write deffff sraka sobaka list range ' 
                      'okay writeln written jack billy comp free liberty foxtrot amazon google ' 
                      'valka krenevich danil danylo rather will winner vishalka yop twoy matj kapec ' 
                      'mama papa daddy zhopa zopa monitor linux vanya starcraft warcraft winn loose ' 
                      'kot kit geek la cho ty takiy dibil computer valik roma default minner war hor ' 
                      'geers fuck mother father futher shot shit egegey gay gays candie pycharm python ' 
                      'len random ascii lowercase itertools testttt gooooooogle compuuuuuter korzhik ' 
                      'lower upper gigigigi univer davidas course finish finished fish fishing kill ' 
                      'killer wayout in out full permutation desk klementine sanya sony motorola ' 
                      'samsung lg fly flying zozula zing zand zant link system siski document idealno '
                      'math physic chemistry calculus limit enumerate durak dodik deniel lana monkey '
                      'mint open close mouse muse joke juke joker fecalii ukraine rus russia sugar'.split()))

n = len(LIST_WORDS)


def test(str1, str2):
    t = 0
    for l in range(len(str1)):
        if str1[l] != str2[l]:
            t += 1
    return t


with open('input.txt', 'w', encoding='utf-8') as file:
    file.write(str(n) + '\n')
    for word in LIST_WORDS:
        file.write(word + '\n')
    index = 0
    for i, permute in enumerate(itertools.permutations(ascii_lowercase[::-1])):
        flag = test(ascii_lowercase, permute)
        if flag < 10:
            continue
        index += 1
        tmp_dict = {}
        for j in range(len(ascii_lowercase)):
            tmp_dict[ascii_lowercase[j]] = permute[j]
        result = ''
        k = random.randrange(1, n)
        for j in range(k):
            tmp = random.randrange(n)
            for letter in LIST_WORDS[tmp]:
                result += tmp_dict[letter]
            result += ' '

        file.write(result + '\n')

        if index > 50:
            break
