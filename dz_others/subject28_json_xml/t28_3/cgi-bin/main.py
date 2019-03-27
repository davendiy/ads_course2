#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t28_2
"""
Дана програма є cgi-скриптом, який приймає на вхід параметри name="string" value=<рядок>,
а на вихід видає html-сторінку з результатами
"""

import cgi
import json
import xml.etree.ElementTree as Et

# вихідна сторінка (код записаний у файлі, для удобства)
with open('cgi-bin/html_page.html', 'r') as html_file:
    HTML_PAGE = html_file.read()


def string_handler(string):
    """ Виділяє з рядку окремо всі цифри й інші символи, зберігаючи порядок

    :param string: рядок
    :return: рядок з цифр, рядок з інших символів
    """
    res1 = ''.join(filter(lambda a: a.isnumeric(), string))
    res2 = ''.join(filter(lambda a: a not in res1, string))
    return res1, res2


def search_json(string):
    """
    функція, яка повертає результати попередної у форматі json

    :param string: рядок
    :return: рядок у форматі json
    """
    res1, res2 = string_handler(string)

    return json.dumps([{'name': 'all the numbers', 'val': res1},
                       {'name': 'other symbols', 'val': res2}], ensure_ascii=True, indent=4)


def search_xml(string, filename='result.xml'):
    """
    функція, яка повертає результати попередніх у форматі xml

    :param string: рядок
    :param filename: назва тимчасового файлу
    :return: рядок у форматі xml
    """

    res1, res2 = string_handler(string)
    # створюємо корінь
    xml_list = Et.Element('result')

    # піддерево позицій
    pos = Et.Element('all the numbers')
    pos.set('val', res1)
    xml_list.append(pos)

    pos2 = Et.Element('other symbols')
    pos2.set('val', res2)
    xml_list.append(pos2)

    # сворюємо загальне дерево і виводимо у файл
    e = Et.ElementTree(xml_list)
    e.write(filename)

    # зчитуємо з файлу і повертаємо як рядок
    with open(filename, 'r') as file:
        res = file.read()
    return res


result1 = ''
result2 = ''

# приймаємо запит
form = cgi.FieldStorage()

# якщо є параметр "string" у запиті - обробляємо його
if 'string' in form:
    tmp_string = form['string'].value
    result1 = search_json(tmp_string)
    result2 = search_xml(tmp_string)

print(HTML_PAGE.format(result1, result2))
