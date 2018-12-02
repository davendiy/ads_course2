#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 02.12.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import tarfile
import sys
import os
import re


pattern = r'_\d\d\d.tar.gz'    # шаблон тома

sep = '\\' if sys.platform == 'win32' else '/'    # символ розділювач в операційній системі


def merge_archive(directory, path_to_save=None):
    """ Злиття томів в один архів

    :param directory: шлях до каталогу з томами
    :param path_to_save: шлях збереження
    """
    if path_to_save is None:    # якщо шлях збереження не вказано, то зберігаємо у тому ж каталозі
        path_to_save = directory

    try:
        os.mkdir(path_to_save)  # спроба створити шлях збереження
    except FileExistsError:
        pass

    file_list = os.listdir(path=directory)   # список файлів каталогу з томами
    filename = ''
    for file in file_list:                   # проходимо по всіх файлах каталогу
        if re.findall(pattern, file):        # шукаємо шаблон тома
            filename = file[:file.rindex('_')]   # якщо знайшли, то запам'ятовуємо ім'я файлу (без номера тома)
            break

    if not filename:  # якщо не знайшли ні одного - вихід з функції
        return

    tarfilename = os.path.join(path_to_save, filename + '.tar.gz')  # ім'я вихідного архіву
    with open(tarfilename, 'wb') as file:      # відкриваємо його в режимі бінарного запису
        i = 0
        while True:
            try:                   # в циклі знаходимо всі томи і додаємо їх до результуючого файлу
                tmp_filename = filename + '_' + '0'*(3-len(str(i))) + str(i) + '.tar.gz'
                tmp_file = open(os.path.join(directory, tmp_filename), 'rb')
                file.write(tmp_file.read())
                tmp_file.close()
                i += 1
            except FileNotFoundError:   # якщо не знайшли - вихід з циклу
                break
    os.chdir(path_to_save)   # переходимо в директорію збереження
    file = tarfile.open(tarfilename, 'r')   # розпаковуємо архів
    file.extractall()
    file.close()


if __name__ == '__main__':
    merge_archive(os.path.join(os.curdir, 'test_out'))
