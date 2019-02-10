#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import os

CHUNK = 1024 * 500


def copyfile(filename, fromdir, tofile):
    """Копіює файл filename з каталогу  fromdir до каталогу todir.
    """
    fromfullpath = os.path.join(fromdir, filename)  # повний шлях до вихідного файлу
    tofullpath = os.path.join(tofile, filename)
    # відкриваємо файли як нетекстові, щоб копіювати будь-які файли
    fromfile = open(fromfullpath, "rb")
    tofile = open(tofullpath, 'wb')
    if os.path.getsize(fromfullpath) <= CHUNK:  # якщо файл невеликий
        cnt = fromfile.read()  # читаємо за один раз
        tofile.write(cnt)
    else:
        while True:
            cnt = fromfile.read(CHUNK)  # інакше читаємо по частинах
            if not cnt:
                break
            tofile.write(cnt)
    fromfile.close()
    tofile.close()


def merge_big_files_dir(path1, path2):
    for root, dirs, files in os.walk(path1):
       for root2, dirs2, files2 in os.walk(path2):
           for file in files:
               if file not in files2:
                    copyfile(file, root, root2)
           break
       break

    for root, dirs, files in os.walk(path2):
        for root2, dirs2, files2 in os.walk(path1):
            for file in files:
                if file not in files2:
                    copyfile(file, root, root2)
            break
        break


