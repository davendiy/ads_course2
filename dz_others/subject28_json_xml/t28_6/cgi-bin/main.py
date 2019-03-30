#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t28_6
"""
Дана програма є cgi-скриптом, який приймає на вхід параметри форми, що заповнює користувач
а на вихід видає html-сторінку з результатами
"""

import cgi
from addition import *

xml = XMLBookLibrary('cgi-bin/refs.xml')

# вихідна сторінка (код записаний у файлі, для удобства)
with open('cgi-bin/html_page.html', 'r') as html_file:
    HTML_PAGE = html_file.read()


def format_result(res_list):
    res = ''
    for el in res_list:
        res += '\n' + ' '.join(el)
    return res


# приймаємо запит
form = cgi.FieldStorage()

# якщо хоч один параметр форми заповнений - обробляємо її
if 'name' in form or 'author' in form or 'from' in form or 'to' in form:

    name = form['name'].value if 'name' in form else ''
    author = form['author'].value if 'author' in form else ''
    year_from = form['from'].value if 'from' in form else ''
    year_to = form['to'].value if 'to' in form else ''

    result1 = format_result(xml.search(name=name,
                                       author=author,
                                       year_from=year_from,
                                       year_to=year_to))

    print(HTML_PAGE.format(result1))
