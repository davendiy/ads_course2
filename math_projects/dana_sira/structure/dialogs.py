#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno, showerror
from .database import *
from .other_functions import *


class DialogAddCategory:
    """ Діалогове вікно для додавання
    категорії транзакцій
    """

    def __init__(self, pre, item_type):
        self.pre = pre            # вікно, яке викликало
        self.type = item_type      # REVENUE or COST
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.grab_set()
        self.diag.title('Add new category')
        self._make_widgets()

    def _make_widgets(self):
        """ Створення віджетів.
        """
        ttk.Label(self.diag, text='Name').grid(row=1, column=1, padx=5, pady=5)
        self._entry = ttk.Entry(self.diag)
        self._entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(self.diag, text='Add', command=self._add).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.diag, text='Cancel', command=self.diag.destroy).grid(row=2, column=2, padx=5, pady=5)

    def _add(self, ev=None):
        """ Обробити натиснення кнопки 'Add'.

        Зчитує з поля для введення назву нової категорії і
        якщо воно не пусте, то намагається додати його до БД.
        """
        tmp_name = self._entry.get()
        if tmp_name:
            try:
                self.pre.data_connector.add_category(tmp_name, self.type)
                showinfo('Success', 'New category is successfully added.')
                self.diag.destroy()
            except Exception as exc:
                showerror('Error', exc)
                print(exc)


class DialogDelCategory:
    """ Діалогове вікно для дидалення
    категорії транзакцій
    """

    def __init__(self, pre, item_type):
        self.pre = pre          # вікно, яке викликало
        self.type = item_type   # REVENUE or COST
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.grab_set()
        self.diag.title('Delete category')
        self._make_widgets()

    def _make_widgets(self):
        ttk.Label(self.diag, text='Name').grid(row=1, column=1, padx=5, pady=5)
        self._entry = ttk.Entry(self.diag)
        self._entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(self.diag, text='Delete', command=self._add).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.diag, text='Cancel', command=self.diag.destroy).grid(row=2, column=2, padx=5, pady=5)

    def _add(self, ev=None):
        """ Обробити натеснення кнопки 'Delete'.

        Запитує користувача підтвердження, зчитує з поля назву категорії
        і намагається видалити таку категорію з бази даних.
        """
        tmp_name = self._entry.get()
        if tmp_name:
            ans = askyesno('Warning', 'Deleting of any category means deleting'
                                      ' all the transactions of this category too')
            if ans:
                try:
                    self.pre.data_connector.delete_category(tmp_name, self.type)
                    showinfo('Success', 'Category is successfully deleted.')
                    self.diag.destroy()
                except Exception as exc:
                    showerror('Error', exc)
                    print(exc)


class DialogAddItem:
    """ Діалог додавання нової транзакції
    """

    def __init__(self, pre, item_type):
        self.pre = pre           # вікно, яке викликало
        self.type = item_type    # REVENUE or COST
        self.diag = Toplevel()
        self._main_frame = Frame(self.diag)
        self._main_frame.pack()
        self.diag.focus_set()
        self.diag.grab_set()
        if item_type == REVENUE:
            self.diag.title('Add new revenue.')
        else:
            self.diag.title('Add new cost.')
        self._make_widgets()

    def _make_widgets(self):

        # для доходів і витрат відповідно свої списки полів (хоча в даному випадку вони однакові)
        fields = REVENUE_FIELDS if self.type == REVENUE else COSTS_FIELDS
        self._entries = {}       # словник, в якому ключі - назва, а значення - відповідні поля для введення

        # словник-перекладач назв категорій в id
        categories = name_dict(self.pre.data_connector.get_categories(self.type))
        i = 0
        for el in fields:
            if el == 'id':     # id не виводимо
                continue
            ttk.Label(self._main_frame, text=el).grid(row=i, column=1, padx=5, pady=5)

            # для категорії замість поля для введення формуємо випадаюче меню
            if el == 'Category':
                # змінна, яка буде відображати вибрану категорію
                self._chosen_category = StringVar(self._main_frame)
                tmp = OptionMenu(self._main_frame, self._chosen_category, *categories.keys())
                tmp.grid(row=i, column=2, padx=5, pady=5)
                ttk.Button(self._main_frame, text='New Category',
                           command=self._new_category).grid(row=i, column=3, padx=5, pady=5)

            # для дати заповнюємо поле для введення сьогоднішньою датою
            elif el == 'Date':
                tmp = ttk.Entry(self._main_frame)
                tmp.insert(0, str(datetime.datetime.now().date()))
                tmp.grid(row=i, column=2, columnspan=2, padx=5, pady=5)
            else:
                tmp = ttk.Entry(self._main_frame)
                tmp.grid(row=i, column=2, columnspan=2, padx=5, pady=5)
            self._entries[el] = tmp
            i += 1

        ttk.Button(self._main_frame, text='Add', command=self._add).grid(row=i, column=1, padx=5, pady=5)
        ttk.Button(self._main_frame, text='Cancel', command=self.diag.destroy).grid(row=i, column=2, padx=5, pady=5)

    def _add(self, ev=None):
        """ Обробити натиснення кнопки 'Add'.

        Зчитує інформацію з полів для введення, перевіряє, чи заповнені обов'язкові
        поля, перевіряє формат введеної інформації (де треба) і додає нову транзакцію
        у відповідну таблицю.
        """
        params = {}       # параметри транзакції - інформація з полів
        translator = name_dict(self.pre.data_connector.get_categories(self.type))
        for key, value in self._entries.items():

            # якщо якесь поле, яке не є коментарем, або категорією пусте, то вихід
            if key not in ['Comments', 'Category'] and not value.get():
                showerror('Error', 'Please, fill all the fields (Comments - optional)')
                return

            if key == 'Category':   # категорія має випадаюче меню, тому її окремо обробляємо
                if not self._chosen_category.get():
                    showerror('Error', 'Please, choose any category')
                    return
                params['Category_id'] = translator[self._chosen_category.get()]

            # дата має задовольняти формат yyyy-mm-dd
            elif key == 'Date':
                tmp = value.get().split('-')
                if len(tmp) != 3 or any([not tmp[0].isdigit(), not tmp[1].isdigit(), not tmp[2].isdigit()]):
                    showerror('Error', 'Please, enter the correct date in format yyyy-mm-dd.')
                    return
                params[key] = value.get()
            else:
                params[key] = value.get()
        params['item_type'] = self.type
        try:
            # завдяки тому, що параметри функції мають ті самі імена, що і поля в таблиці
            # можна використати **
            self.pre.data_connector.add_item(**params)
            showinfo('Success', 'New item is successfully added.')
            self.diag.destroy()
        except Exception as exc:
            showerror('Error', exc)
            print(exc)

    def _new_category(self, ev=None):
        """ Обробити натиснення кнопки 'New category'.

        Викликає діалогове вікно додавання нової категорії.
        """
        tmp = DialogAddCategory(self.pre, self.type)  # викликаємо відповідне вікно
        self.diag.wait_window(tmp.diag)
        self._main_frame.destroy()                    # оновлюємо віджети
        self._main_frame = Frame(self.diag)
        self._main_frame.pack()
        self._make_widgets()


class DialogChangeItem:
    """ Діалогове вікно зміни параметрів транзакції.

    Аналогічне попередньому, окрім того, що у полях для введення уже є
    інформація, витягнута з бази даних + викликає інший метод BudgetCollection
    """

    def __init__(self, pre, item_type, default: dict):
        self.pre = pre
        self.type = item_type
        self.default = default
        self.diag = Toplevel()
        self._main_frame = Frame(self.diag)
        self._main_frame.pack()
        self.diag.focus_set()
        if item_type == REVENUE:
            self.diag.title('Change revenue.')
        else:
            self.diag.title('Change cost.')
        self._make_widgets()

    def _make_widgets(self):
        fields = REVENUE_FIELDS if self.type == REVENUE else COSTS_FIELDS
        self._entries = {}
        categories = name_dict(self.pre.data_connector.get_categories(self.type))
        default_category = self.default['Category']
        i = 0
        for el in fields:
            if el == 'id':
                continue
            ttk.Label(self._main_frame, text=el).grid(row=i, column=1, padx=5, pady=5)
            if el == 'Category':
                _values = tuple(categories.keys())
                self._chosen_category = StringVar(self._main_frame)
                tmp = ttk.OptionMenu(self._main_frame, self._chosen_category, default_category, *_values)
                tmp.grid(row=i, column=2, padx=5, pady=5)
                ttk.Button(self._main_frame, text='New Category',
                           command=self._new_category).grid(row=i, column=3, padx=5, pady=5)
            else:
                tmp = ttk.Entry(self._main_frame)
                tmp.insert(0, self.default[el])
                tmp.grid(row=i, column=2, columnspan=2, padx=5, pady=5)
            self._entries[el] = tmp
            i += 1

        ttk.Button(self._main_frame, text='Change', command=self._change).grid(row=i, column=1, padx=5, pady=5)
        ttk.Button(self._main_frame, text='Delete', command=self._del).grid(row=i, column=3, padx=5, pady=5)
        ttk.Button(self._main_frame, text='Cancel', command=self.diag.destroy).grid(row=i, column=2, padx=5, pady=5)

    def _change(self, ev=None):
        params = {}
        translator = name_dict(self.pre.data_connector.get_categories(self.type))
        for key, value in self._entries.items():
            if key not in ['Comments', 'Category'] and not value.get():
                showerror('Error', 'Please, fill all the fields (Comments - optional)')
                return

            if key == 'Category':
                if not self._chosen_category.get():
                    showerror('Error', 'Please, choose any category')
                    return
                params['Category_id'] = translator[self._chosen_category.get()]
            elif key == 'Date':
                tmp = value.get().split('-')
                if len(tmp) != 3 or any([not tmp[0].isdigit(), not tmp[1].isdigit(), not tmp[2].isdigit()]):
                    showerror('Error', 'Please, enter the correct date in format yyyy-mm-dd.')
                    return
                params[key] = value.get()
            else:
                params[key] = value.get()
        params['item_type'] = self.type
        params['id'] = self.default['id']
        try:
            self.pre.data_connector.change_item(**params)
            showinfo('Success', 'Item is successfully changed.')
            self.diag.destroy()
        except Exception as exc:
            showerror('Error', exc)
            print(exc)

    def _new_category(self, ev=None):
        tmp = DialogAddCategory(self.pre, self.type)
        self.diag.wait_window(tmp.diag)
        self._main_frame.destroy()
        self._main_frame = Frame(self.diag)
        self._main_frame.pack()
        self._make_widgets()

    def _del(self, ev=None):
        ans = askyesno('Warning', 'Do you really want to delete this item?')
        if ans:
            try:
                self.pre.data_connector.delete_item(self.default['id'], self.type)
                showinfo('Success', 'Item is successfully deleted')
                self.diag.destroy()
            except Exception as e:
                showerror('Error', e)
                print(e)
