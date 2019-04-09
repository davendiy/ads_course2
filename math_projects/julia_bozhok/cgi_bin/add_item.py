#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Додати елемент до бази даних"""

from bin import *
import cgi

form = cgi.FieldStorage()

# працює тільки за умови, що всі поля заповнені
if all([param in form for param in ADD_PARAMS]):

    # формуємо словник з параметрів
    data = {param: form[param].value for param in ADD_PARAMS}
    translator = name_dict(data_connector.get_categories())     # для заміни назви категорії на її id

    # перевірка чи всі необхідні поля є числовими
    if any(not data[el].isnumeric() for el in ['Build_number', 'Shelf_number', 'Department_id']):
        showerror('Please, enter the correct data')
        exit(1)

    # якщо назва категорії не у базі даних, необхідно додати нову категорію з таким ім'ям
    if data['Category'] not in translator:
        data_connector.add_category(data['Category'])
        translator = name_dict(data_connector.get_categories())

    data['Category_id'] = translator[data['Category']]   # заміна id на name
    del data['Category']

    # через те, що назви полів і ключових змінних однакові - можна використовувати **
    data_connector.add_item(**data)

    with open(HOME_PAGE_PATTERN, 'r', encoding='utf-8') as file:
        page = file.read()

    # оновлення домашньої сторінки і виведення її на екран
    data = data_connector.find_item('')
    categories = data_connector.get_categories()
    translator = id_dict(categories)
    for el in data:
        el['Category'] = translator[el['Category_id']]
        del el['Category_id']

    page = fill_cr_page(page, data)
    with open(HOME_PAGE, 'w', encoding='utf-8') as file:
        file.write(page)

    print(change_html(page, mode=STRING_MODE))

else:
    showerror('Please, fill all the fields.')
