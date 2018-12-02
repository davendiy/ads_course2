#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 02.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import tarfile
import os
import sys

sep = '\\' if sys.platform == 'win32' else '/'   # символ розділювач в операційній системі

CHUNK = 100 * 1024


def archive(directory: str, path_to_save: str, chunk=CHUNK):1
    """ Архівування каталогу і розбиття його на
    томи, якщо результуючий розмір файлу перевищує
    заданий

    :param directory: шлях до каталогу
    :param path_to_save: шлях збереження
    :param chunk: заданий розмір файлу
    """
    n = directory.rindex(sep)      # індекс останнього символа-розділювача (щоб відокремити назву каталогу)
    tarfilename = directory[n+1:] + '.tar.gz'   # назва вихідного архіву
    filepath = os.path.join(path_to_save, tarfilename)  # абсолютний шлях до файлу

    try:
        os.mkdir(path_to_save)     # створення каталогу збереження, якщо можливо
    except FileExistsError:
        pass

    tar = tarfile.open(filepath, 'w:gz')   # створення архіву
    os.chdir(directory[:n])                # переходимо до каталогу, де знаходиться необхідний каталог
    tar.add('.' + directory[n:])           # додаємо крапку, щоб архіватор не зберігав абсолютний шлях
    tar.close()

    if os.path.getsize(filepath) > chunk:   # якщо розмір перевищує заданий
        with open(filepath, 'rb') as file:  # відкриваємо архів у режимі бінарного читання
            i = 0
            while True:
                tmp = file.read(chunk)     # зчитуємо дану к-ть байтів
                if not tmp:                # якщо вже нема що зчитувати - вихід з циклу
                    break
                n = tarfilename.index('.tar.gz')   # індекс, до якого ім'я файлу без розширення
                # створення ім'я і-го тома
                tmp_name = tarfilename[:n] + '_' + '0'*(3-len(str(i))) + str(i) + '.tar.gz'
                tmp_name = os.path.join(path_to_save, tmp_name)
                tmp_file = open(tmp_name, 'wb')             # запис в бінарний файл і-го тома
                tmp_file.write(tmp)
                tmp_file.close()
                i += 1
        os.remove(filepath)    # видалення великого архіву


if __name__ == '__main__':
    archive(os.path.join(os.curdir, 'test'), os.path.join(os.curdir, 'test_out'))
