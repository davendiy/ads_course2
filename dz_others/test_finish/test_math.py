#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 06.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import os
import tarfile

CHUNK = 10 * 1024 * 1024


def archive(directory):

    for root, paths, filenames in os.walk(directory):

        for file in filenames:
            filename, extens = os.path.splitext(file)
            if extens == '.docx' and os.path.getsize(file) > CHUNK:
                os.chdir(root)
                tar = tarfile.open(filename+".tar.gz", 'w:gz')
                tar.add(file)
                tar.close()


def cpp(directory):
    for root, paths, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.cpp'):
                os.chdir(root)
                file = open(filename, 'r')
                inform = file.readlines()
                file.close()
                file = open(filename, 'w')
                for line in inform:
                    if '//' not in line:
                        file.write(line + '\n')

                    tmp = line.index('//')
                    line = line[:tmp] + '/*' + line[tmp+2:] + '*/'
                    file.write(line + '\n')
                file.close()


def polynomial(directory):
    res = 0
    for root, paths, filenames in os.walk(directory):
        for filename in filenames:
            os.chdir(root)
            try:
                file = open(filename, 'r')
                inform = file.read()
                if inform.replace(' ', '').isalnum():
                    del inform
                    for line in file:
                        degree, coeff = map(int, line.split())
                        res += coeff * 2 ** degree
                file.close()
                break
            except Exception as e:
                print(e)
                pass
    return res

