#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 01.03.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from math_projects.diana_vitv.bin import *
import sys
import tkinter as tk
import datetime

with open('logs.log', 'a') as file:
    sys.stdout = file
    sys.stderr = file
    print("===================={}=====================".format(datetime.datetime.now()))
    top = tk.Tk()
    test = MainWindow(top)
    test.mainloop()
    print()
    print()
