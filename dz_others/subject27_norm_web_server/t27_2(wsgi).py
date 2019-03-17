#!/usr/bin/env python3
# -*-encoding: utf-8-*-

#
# t27_2
# пошук к-ті змін знаків у послідовності

import cgi

# тіло HTML сторінки, на якій все буде відбуватись
HTML_PAGE = """<html>
<title>Перевірка, чи є рядок паліндромом</title>
<body>
<h3>Перевірка заданого рядка</h3>
<br>
{}
<br>
<br>
<form method=POST action="">
<table>
<tr>
<td align=right>
<font size="5" color="blue" face="Arial">
Введіть рядок:
</font>
</td>
<td>
<input type=text name=string value="">
</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="Перевірити">
</td>
<table>
</form>
</body>
</html>
"""


def ispalindrom(string):
    """
    функція, яка перевіряє, чи є рядок паліндромом

    :param string: рядок
    :return: булеве значення (чи дорівнює рядок перевернутому собі
    """
    return string == string[::-1]


def application(environ, start_response):
    """Викликається WSGI-сервером.

       Отримує оточення environ та функцію,
       яку треба викликати у відповідь: start_response.
       Повертає відповідь, яка передається клієнту.
    """
    if environ.get('PATH_INFO', '').lstrip('/') == '':
        # отримати словник параметрів, переданих з HTTP-запиту
        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                                environ=environ)
        result = ''
        # перевіряємо чи є параметр string у запиті
        if 'string' in form:

            # якщо є, обробляємо його
            tmp_string = form['string'].value
            result = ispalindrom(tmp_string)

        # в тіло HTML сторінки додаємо result
        body = HTML_PAGE.format(result)
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        # якщо команда невідома, то виникла помилка
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        body = 'Сторінку не знайдено'
    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':
    # створити та запуститити WSGI-сервер
    from wsgiref.simple_server import make_server

    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()
