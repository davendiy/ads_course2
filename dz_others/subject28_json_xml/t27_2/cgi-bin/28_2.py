#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t28_2
"""
Дана програма є cgi-скриптом, який приймає на вхід параметри name="string" value=<рядок>,
                                                             name='letter' value=<символ>
а на вихід видає html-сторінку з посиланнями на вихідні json та xml файли
"""

import cgi
import json
import xml.etree.ElementTree as Et

# вихідна сторінка (код записаний у файлі, для удобства)
with open('cgi-bin/html_page.html', 'r') as html_file:
    HTML_PAGE = html_file.read()


def search_letter(string, letter):
    """
    функція, яка знаходить всі позиції символа у рядку
    :param string: рядок
    :param letter: символ
    :return: список цілих чисел (позиції)
    """
    pos = []
    for i, temp_letter in enumerate(string):
        if temp_letter == letter:
            pos.append(i)
    return pos


def search_max_seq(string):
    """
    функція, яка у рядку знаходить найдовшу послідовність з однакових символів
    :param string: рядок
    :return: кортеж(символ, який утворює послідовність; максимальна довжина)
    """
    max_count = 0
    max_letter = ''
    tmp_count = 0

    # проходимо по всіх символах
    for i in range(len(string) - 1):
        # поки символи однакові збільшуємо довжину послідовності
        if string[i] == string[i + 1]:
            tmp_count += 1

        # якщо послідовність закінчилась, перевіряємо, чи більша її довжина за максимальну
        elif string[i] != string[i + 1] and tmp_count > max_count:
            max_count = tmp_count
            max_letter = string[i]
            tmp_count = 0
        # якщо ні, то просто обнуляємо довжину
        else:
            tmp_count = 0
    # перевіряємо останню послідовність, оскільки в циклі вона може не закінчитись
    if tmp_count > max_count:
        max_count = tmp_count
        max_letter = string[-1]
    return max_letter, max_count


def search_json(string, letter, filename='result.json'):
    """
    функція, яка повертає результати попередніх у форматі json

    :param string: рядок
    :param letter: символ
    :param filename: назва вихідного файлу
    :return: назва вихідного файлу
    """
    result_letter = search_letter(string, letter)
    max_letter, max_count = search_max_seq(string)

    with open(filename, 'w') as file:
        json.dump([result_letter, (max_letter, max_count)], file, ensure_ascii=True, indent=4)
    return filename


def search_xml(string, letter, filename='result.xml'):
    """
    функція, яка повертає результати попередніх у форматі xml

    :param string: рядок
    :param letter: символ
    :param filename: назва вихідного файлу
    :return: назва вихідного файлу
    """
    result_pos = search_letter(string, letter)
    max_letter, max_count = search_max_seq(string)

    # створюємо корінь
    xml_list = Et.Element('result')

    # піддерево позицій
    pos = Et.Element('letter_position')
    for tmp_pos in result_pos:
        tmp_xml = Et.Element('position')
        tmp_xml.set('pos', str(tmp_pos))
        pos.append(tmp_xml)

    xml_list.append(pos)

    # піддерево макс послідовності
    max_xml = Et.Element('max_sequence')
    max_xml.set('letter', max_letter)
    max_xml.set('len', str(max_count))
    xml_list.append(max_xml)

    # сворюємо загальне дерево і виводимо у файл
    e = Et.ElementTree(xml_list)
    e.write(filename)
    return filename


result1 = ''
result2 = ''

# приймаємо запит
form = cgi.FieldStorage()

# якщо є параметр "string" і "letter" у запиті - обробляємо його
if 'string' and 'letter' in form:
    tmp_string = form['string'].value
    tmp_letter = form['letter'].value
    result1 = search_json(tmp_string, tmp_letter)
    result2 = search_xml(tmp_string, tmp_letter)

# у вихідній сторінці необхідно шлях до файлів доповнити їхньою назвою і саме гіперпосилання назвати ім'ям файлу
print(HTML_PAGE.format(result1, result1, result2, result2))
