#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from bin import *
from time import sleep
import sys
import logging

logging.basicConfig(filename=DEFAULT_LOG_CLIENT, format=FORMAT, level=logging.DEBUG)


if len(sys.argv) == 1:
    sleeptime = int(SLEEP * 3600)
else:
    sleeptime = int(sys.argv[1] * 3600)

while True:         # моніторинг з певним періодом
    print('starting parse...')
    try:
        monitoring()
        print('successful')
    except Exception as e:
        logging.exception(e)
        print('ends')
    sleep(sleeptime)
