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
ERROR_PAGE = 'front/error_page.html'

DIALOG_REC_PATTERN = 'front/dialog_add_record.html'

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

START_ADDING = 'Add'   # параметр методу POST, який вказує, що додавання запису тільки починається
END_ADDING = 'Submit'       # параметр методу POST, який вказує, що додавання запису закінчується

# Список полів з таблиці REVENUE, які будуть відображатись у GUI
REVENUE_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

# Список полів з таблиці COST, які будуть відображатись у GUI
COSTS_FIELDS = ('id', 'Date', 'Sum', 'Category', 'Comments')

COMMENTS = 'Comments'    # поле коментарі

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
