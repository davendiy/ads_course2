#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# t27_4
# знайти к-ть змін знаку

import cgi

# html-сторінка, яку програма буде надсилати

with open('cgi-bin/html_page.html', 'r') as html_file:
    HTML_PAGE = html_file.read()


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


result = ''

# створюємо об'єкт класу FieldStorage для роботи з запитами
form = cgi.FieldStorage()

# перевіряємо, чи є параметр "seq" у запиті
if 'seq' in form:

    # якщо є, то зчитуємо його значення і перевіряємо
    tmp_string = form['seq'].value
    result = count_change(tmp_string)

# надсилаємо html сторінку у відповідь
print(HTML_PAGE.format(result))
