#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from math_projects.diana_vitv.bin import *
import sys
import tkinter as tk
import datetime

with open('logs.log', 'a') as file:
    # sys.stdout = file
    # sys.stderr = file
    print("===================={}=====================".format(datetime.datetime.now()))
    top = tk.Tk()
    test = MainWindow(top)
    test.mainloop()
    print()
    print()
