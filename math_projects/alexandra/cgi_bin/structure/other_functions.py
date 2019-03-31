#!/usr/bin/env python3
# -*-encoding: utf-8-*-


# шляхи до html сторінок
HOME_PAGE = 'front/home_page.html'
COSTS_PAGE = 'front/costs_page.html'
REVENUE_PAGE = 'front/revenue_page.html'

# шляхи до шаблонів html сторінок
HOME_PAGE_PATTERN = 'front/home_page_pattern.html'
COSTS_PAGE_PATTERN = 'front/costs_page_pattern.html'
REVENUE_PAGE_PATTERN = 'front/revenue_page_pattern.html'

DIAGRAM_PATTERN = 'front/diagram.html'


STYLE_SHEET = 'front/style.css'        # шлях до css файлу

DIAGRAM_COSTS = 'diagram_costs.png'      # шлях до файлу, куди буде збережено діаграму
DIAGRAM_REVENUES = 'diagram_revenues.png'

# параметри, які необхідно вставляти в домашню сторінку
HOME_PAGE_PARAMS = ('costs_day',
                    'costs_month',
                    'revenues_month',
                    'balance')

# параметри, які необхідно вставляти в сторінку створення нового запису
DIALOG_PAGE_PARAMS = ('type',
                      'cur_date')

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
DEFAULT_DATABASE = 'budget.db'

# параметри, які надсилає сторінка з витратами або доходами через метод POST
POST_PARAMS = ['Day', 'Month', 'Year', 'Category', 'All_time']

# html опис рядка таблиці
HTML_PIECE = """
            <tr>
                <td>{id}</td>
                <td>{Date}</td>
                <td>{Sum}</td>
                <td>{Category}</td>
                <td>{Comments}</td>
            </tr>
"""

FILE_MODE = 'file'
STRING_MODE = 'string'


def change_html(filename_or_page, mode=FILE_MODE):
    """ Прочитати html сторінку і змінити її у формат,
    який буде надсилати cgi скрипт

    :param filename_or_page: назва файлу
    :param mode: вказує в якому режимі працює функція: FILE_MODE - на вхід дано назву файлу
                                                       STRING_MODE - на вхід дано рядок
    :return: рядок
    """

    # замінюємо <!DOCTYPE html> на Content-type: text/html charset=utf-8\n\n
    if mode == FILE_MODE:
        with open(filename_or_page, 'r', encoding='utf-8') as file:
            text = file.read().strip()
    else:
        text = filename_or_page
    text = text.replace('<!DOCTYPE html>', 'Content-type: text/html charset=utf-8\n\n')

    # вставляємо в <head> замість <link rel="stylesheet" href="style.css"> дані з css файла
    with open(STYLE_SHEET, 'r', encoding='utf-8') as file:
        style = file.read()

    style = '<style>' + style + '</style>'
    text = text.replace('<link rel="stylesheet" href="style.css">', style)

    text = text.replace('home_page.html', '../front/home_page.html')
    text = text.replace('costs_page.html', '../front/costs_page.html')
    text = text.replace('revenue_page.html', '../front/revenue_page.html')
    return text


def fill_page(page: str, list_values: list) -> str:
    """ Додати в html текст рядки таблиці

    В html паттерні сторінки (revenue_page_pattern.html i costs_page_pattern.html)
    таблиця з результатми містить тільки заголоки, після яких стоїть коментар <!-- {} -->
    замість цього коментаря необхідно вставити код, який імплементуватиме рядок таблиці

    :param page: рядок з html кодом, в якому наявний '<!-- {} -->'
    :param list_values: [{"Sum": ...,
                          "Id": ...,
                          "Category: ...,
                          "Date": ...,
                          "Comments": ...}] - список словників, які повертає BudgetCollection
    :return:
    """
    tmp = ''
    for el in list_values:
        tmp += HTML_PIECE.format(**el)         # формуємо послідовність рядків таблиці
    return page.format(tmp)


def name_dict(dicts_list) -> dict:
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {Name: id}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(Name1: id1, Name2: id2)
    """
    res = {}
    for el in dicts_list:
        res[el['Name']] = el['id']
    return res


def id_dict(dicts_list):
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {id: Name}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(id1: Name1, id2: Name2)
    """
    res = {}
    for el in dicts_list:
        res[el['id']] = el['Name']
    return res


def fill_home(page, costs_day=0, costs_month=0, revenue_month=0, balance=0):
    return page.format(costs_day=costs_day,
                       costs_month=costs_month,
                       revenues_month=revenue_month,
                       balance=balance)

if __name__ == '__main__':
    print(change_html('/files/univer/python/course2/math_projects/alexandra/front/home_page.html'))
