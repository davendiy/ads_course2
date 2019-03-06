#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Головна програма.
"""

from math_projects.alina_merz.bin import *
import sys
import tkinter as tk
import datetime

# перенаправляюємо стандартні потоки stdout (виведення) i stderr (виведення помилок)
# у відповідні лог-файли.
file_print = open('messages.log', 'a', encoding='utf-8')
file_errors = open('errors.log', 'a', encoding='utf-8')

sys.stdout = file_print
sys.stderr = file_errors

try:
    # відповідно тепер кожен print буде виводитись у messages.log
    print("===================={}=====================".format(datetime.datetime.now()))
    file_errors.write("===================={}====================\n".format(datetime.datetime.now()))
    top = tk.Tk()
    top.title('Аліна Мерзлякова')
    test = MainWindow(top)
    test.mainloop()
    print()
    print()
except Exception as e:
    # а кожна помилка буде виводитись у errors.log
    file_errors.write(str(e))
    file_errors.close()
    file_print.close()
