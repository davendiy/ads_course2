#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkol
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

# T22_11_v3
# Збереження файлів з заданих каталогів (backup)
# Усі попередні версії backup архівуються
# Використовується shutil для копіювання та видалення каталогів

import os
import datetime
import shutil


def getbackupname(backupdir):
    """Будує ім'я каталогу для backup у backupdir.

       Ім'я створюється як рядок поточного часу
    """
    dt = datetime.datetime.now()
    dirname = dt.strftime('%Y%m%d_%H%M%S')  # формуємо ім'я каталогу за поточним часом
    return os.path.join(backupdir, dirname)


def archivesubdirs(directory):
    """Створює архіви підкаталогів у dir.

       Після створення архіву відповідний підкаталог видаляється
    """
    lst = os.listdir(directory)  # отримуємо вміст каталогу
    for item in lst:
        fullitem = os.path.join(directory, item)  # повний шлях до елементу каталогу
        if os.path.isdir(fullitem):  # якщо каталог то архівуємо його
            try:
                # створюємо архівний файл зі стисненням у форматі gzip
                shutil.make_archive(fullitem, 'gztar', fullitem)
                shutil.rmtree(fullitem)  # видаляємо заархівований підкаталог
            except Exception as e:
                print('archivesubdirs: skipping', item, e)  # пропускаємо підкаталог, якщо помилка


def backupdirectories(directories, backupdir):
    """Створює backup даних з directories у backupdir.

    """
    archivesubdirs(backupdir)  # архівуємо попередні версії
    toparent = getbackupname(backupdir)
    for directory in directories:
        try:
            last = os.path.split(directory)[-1]       # last - остання частина шляху - ім'я катлогу
            todir = os.path.join(toparent, last)
            shutil.copytree(directory, todir)
        except Exception as e:
            print('backupdirectories: skipping', directory, e)  # пропускаємо каталог, якщо помилка


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:  # якщо не вистачає параметрів, ввести
        test_backupdir = input("Backup directory: ")
        test_directories = input("Directories to backup: ").split()
    else:
        test_backupdir = sys.argv[1]  # 1 параметр
        test_directories = sys.argv[2:]  # параметри, починаючи з 2
    backupdirectories(test_directories, test_backupdir)
