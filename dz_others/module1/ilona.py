#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import os

CHUNK = 1024 * 500


def merge_big_files(dir, files):
    for name in files:
        if '001' in name:
            outname = name.replace('001', '')
            tmp = outname.rindex('.')
            output = open(os.path.join(dir, name), 'wb')
            i = 1
            while True:
                tmp_name = outname[:tmp] + '0' * (3 - len(str(i))) + outname[tmp:]
                if tmp_name in files:
                    copyfile(tmp_name, dir, output)
                else:
                    break
                i += 1
            output.close()


def copyfile(filename, fromdir, tofile):
    """Копіює файл filename з каталогу  fromdir до каталогу todir.
    """
    fromfullpath = os.path.join(fromdir, filename)  # повний шлях до вихідного файлу
    # відкриваємо файли як нетекстові, щоб копіювати будь-які файли
    fromfile = open(fromfullpath, "rb")

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


def merge_big_files_dir(path):
    for root, dirs, files in os.walk(path):
        merge_big_files(root, files)


if __name__ == '__main__':
    test_path = input("шлях: ")
    copyfile(test_path)
