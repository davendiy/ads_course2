#!/usr/bin/env python
# -*-encoding: utf-8-*-

# by David Zashkol
# 1 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

# t27_11_fib_web_v1.py
# Обчислення чисел Фібоначчі через веб-сервер.

import cgi

HTML_PAGE = """Content-type: text/html charset=utf-8\n\n
<html>
<head>
    <meta charset="UTF-8">
    <title>Title</title>

<title>Обчислення чисел Фібоначчі</title>
</head>
<body>
<h3>Обчислення заданого числа Фібоначчі</h3>
<br>
{}
<br>
<form method=POST action="http://localhost:8000/cgi-bin/t27_11_fib_web_v2.py">
<p>Введіть номер числа Фібоначчі:
<input type=text name=n_val value="">
<input type=submit value="Обчислити">
</p>
</form>
</body>
</html>
"""

def fib(n):
    """Обчислює n-те число Фібоначчі."""
    a, b = 1, 1
    for i in range(n):
        a, b = b, a + b
    return a

result = ''

form = cgi.FieldStorage()
if 'n_val' in form:
    n = int(form['n_val'].value)
    result = 'Fib({}) = {}'.format(n, fib(n))

print(HTML_PAGE.format(result))
