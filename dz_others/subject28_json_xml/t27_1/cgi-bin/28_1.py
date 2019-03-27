#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t28_1
"""
Дана програма є cgi-скриптом, який приймає на вхід параметр name="string" value=<рядок>, а на вихід видає
html-сторінку з посиланнями на вихідні json та xml файли
"""

import cgi
import json
import xml.etree.ElementTree as Et

# вихідна сторінка
HTML_PAGE = """Content-type: text/html charset=utf-8\n\n
<html>
<head>
    <meta charset="UTF-8">
    <title>Title</title>

<title>Розбиття рядку на слова</title>
</head>
<body>
<h3>Розбиття даного рядка</h3>
<br>
RESULT_JSON: <a href="http://localhost:8001/{}"> {} </a>
</br>
<br>
RESULT XML: <a href='http://localhost:8001/{}'> {} </a> 
</br>
<form method=POST action="http://localhost:8000/cgi-bin/28_1.py">
<p>Введіть рядок:
<input type=text name=string value="">
<input type=submit value="Розбити">
</p>
</form>
</body>
</html>
"""


def split_json(string, filename="result.json"):
    """
    функція, яка розбиває рядок на слова у форматі json

    :param string: рядок
    :param filename: ім'я вихідного файлу
    :return: ім'я вихідного файлу
    """

    # розбиваємо рядок на слова і перетворюємо його в множину, щоб слова не повторювались
    tmp_list = set(string.split())
    result_list = []

    # перетворюємо множину на список словників
    for j, word in enumerate(tmp_list):
        result_list.append({"number": j, "word": word})

    # записуємо у форматі json у вихідний файл
    with open(filename, 'w') as file:
        json.dump(result_list, file, ensure_ascii=True, indent=4, sort_keys=lambda a: a["number"])
    return filename


def split_xml(string, filename="result.xml"):
    """
    функція, яка розбиває рядок на слова у форматі xml

    :param string: рядок
    :param filename: ім'я вихідного файлу
    :return: ім'я вихідного файлу
    """

    # аналогічно розбиваємо рядок на множину слів
    tmp_list = set(string.split())

    # створюємо корінь
    xml_list = Et.Element('list_of_words')

    # проходимо по всіх словах і створюємо відповідні вузли, як це робиться у програмі 28_21_refbook_xml.py
    for i, word in enumerate(tmp_list, 1):
        tmp_word = Et.Element('word')
        tmp_word.set("number", str(i))
        tmp_word.text = word
        xml_list.append(tmp_word)

    # створюємо об'єкт xml і записуємо його у файл
    e = Et.ElementTree(xml_list)
    e.write(filename)
    return filename


result1 = ''
result2 = ''

# приймаємо запит
form = cgi.FieldStorage()

# якщо є параметр "string" у запиті - обробляємо його
if 'string' in form:
    tmp_string = form['string'].value
    result1 = split_json(tmp_string)
    result2 = split_xml(tmp_string)

# у вихідній сторінці необхідно шлях до файлів доповнити їхньою назвою і саме гіперпосилання назвати ім'ям файлу
print(HTML_PAGE.format(result1, result1, result2, result2))
