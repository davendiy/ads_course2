#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import re
import os
import datetime
from docx import Document

DT = r'\d{2}\.\d{2}\.\d{4}'

now_date = datetime.datetime.now().strftime('%d.%m.%Y')


def find_dates(filename):
    """
    шукає усі дати у форматі dd.mm.yyyy у файлі MS docx
    + замість __.__.____ вставляє поточну дату
    :param filename: назва файлу
    """

    document = Document(filename)
    res = []
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            text = run.text
            res += re.findall(DT, text)        # знаходимо усі дати у форматі dd.mm.yyyy

            text = text.replace(r'__.__.____', now_date)   # заміняємо підкреслення поточною датою
            run.text = text

    fname, ext = os.path.splitext(filename)  # розбити повне ім'я файлу
    fname += '_'
    newfilename = fname + ext  # додати до імені файлу підкреслення
    document.save(newfilename)  # зберегти документ
    return res


if __name__ == '__main__':

    print(find_dates('t23_4.docx'))
