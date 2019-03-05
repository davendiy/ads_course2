#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# author: Oleksandr Obvintsev

""" Пакет t23_21 - приклад з лекцій.
T23_23
Злиття даних з файлів MS Word, MS Excel за шаблоном MS Word
Імена полів, що заповнюються даними, мають бути взяті у фігурні дужки { }
Файли, з яких треба брати дані, вказують у конфігураційному файлі
(в проекті конфігураційний файл не використовується).
"""

from .merge_doc_xls import *
from .sourceitem import *
from .mergesource import *


__all__ = ['Merger', 'MergeSource', 'SourceItem']
