#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from math_projects.kateryna.bin import *

# curs = data_conn.get_cursor()
# curs.execute('DELETE FROM Links')
# data_conn.close()

logging.basicConfig(filename=DEFAULT_LOG_GUI, format=FORMAT, level=logging.DEBUG)

test = MainWindow()
test.mainloop()
