#!/usr/bin/env python3
# -*-encoding: utf-8-*-

HOME_PAGE = '/front/home_page.html'
COSTS_PAGE = '/front/costs_page.html'
REVENUE_PAGE = '/front/revenue_page.html'

HOME_PAGE_PARAMS = ('costs_day',
                    'costs_month',
                    'revenues_month',
                    'balance')


# Список полів з таблиці REVENUE, які будуть відображатись у GUI
REVENUE_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

# Список полів з таблиці COST, які будуть відображатись у GUI
COSTS_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

# К-ть елементів за умовчанням, які буде видавати пошук
DEFAULT_N = 40

# Константа, що означає тип транзакції 'Дохід'. Збігається з назвою таблиці з доходами
REVENUE = 'Revenues'

# Константа, що означає тип транзакції 'Витрата'. Збігається з назвою таблиці з витратами
COST = 'Costs'

# шлях за умовчанням до бази даних
DEFAULT_DATABASE = './budget.db'


def change_html(filename):
    """ Прочитати html сторінку і змінити її у формат,
    який буде надсилати cgi скрипт

    :param filename: назва файлу
    :return: рядок
    """
    text = ''
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().strip()
        text = text.lstrip('<!DOCTYPE html>')
        text = 'Content-type: text/html charset=utf-8\n\n' + text

    return text


if __name__ == '__main__':
    print(change_html('/files/univer/python/course2/math_projects/alexandra/front/home_page.html'))
