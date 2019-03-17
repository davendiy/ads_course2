#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t27_2
# перевірка, чи є рядок паліндромом через CGI сервер

import cgi

# html-сторінка, яку програма буде надсилати

HTML_PAGE = """Content-type: text/html charset=utf-8\n\n
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Перевірка чи є рядок паліндромом</title>
</head>
<body>
    <h3>Перевірка даного рядка</h3>
    Результат: {}
    <form method=POST action="t27_2.py">
        <p>Введіть рядок:
            <label>
                <input type=text name=string value="">
            </label>
            <input type=submit value="Перевірити">
        </p>
    </form>
</body>
</html>"""


def ispalindrom(string):
    """
    функція, яка перевіряє, чи є рядок паліндромом

    :param string: рядок
    :return: булеве значення (чи дорівнює рядок перевернутому собі
    """
    return string == string[::-1]


result = ''

# створюємо об'єкт класу FieldStorage для роботи з запитами
form = cgi.FieldStorage()

# перевіряємо, чи є параметр "string" у запиті
if 'string' in form:

    # якщо є, то зчитуємо його значення і перевіряємо
    tmp_string = form['string'].value
    result = ispalindrom(tmp_string)

# надсилаємо html сторінку у відповідь
print(HTML_PAGE.format(result))
