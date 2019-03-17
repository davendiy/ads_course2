#!/usr/bin/env python
# -*-encoding: utf-8-*-

# t27_4
# знайти к-ть змін знаку у числовій послідовності

import cgi

# тіло HTML сторінки, на якій все буде відбуватись
HTML_PAGE = """<html>
<title>Пошук к-ть змін знаків</title>
<body>
<h3>Пошук к-ть змін знаків</h3>
<br>
{}
<br>
<br>
<form method=POST action="">
<table>
<tr>
<td align=right>
<font size="5" color="blue" face="Arial">
Введіть послідовність цілих чисел через кому:
</font>
</td>
<td>
<input type=text name=string value="">
</td>
<tr>
<td colspan=2 align=center>
<input type=submit value="Обробити">
</td>
<table>
</form>
</body>
</html>
"""


def count_change(string):
    """
    функція, яка рахує к-ть змін знаків у числовій послідовності, заданої рядком
    :param string: рядок
    :return: ціле число - к-ть
    """
    num_list = string.split(',')
    count = 0
    pre_numb = '0'
    # проходимо по всіх числах
    for number in num_list:

        # якщо добуток сусідніх чисел < 0, то вони мають різні знаки
        if int(pre_numb) * int(number) < 0:
            count += 1
        elif number == '0':
            break
        pre_numb = number
    return count


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
            result = count_change(tmp_string)

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
    print("http://localhost:8000")
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()
