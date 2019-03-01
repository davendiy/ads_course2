#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 01.03.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from tkinter import *
# from .main_window import MainWindow
from tkinter.messagebox import showerror
import datetime

# TODO діалог видалення і додавання категорії
# TODO діалог відкриття діректорії зберігання і т.п.
# TODO діалог створення звіту


def sql2dict(dicts_list):
    res = {}
    for el in dicts_list:
        res[el['Name']] = el['id']
    return res


class DialogEnter:
    """ Діалогове вікно введення нового товару.
    """

    def __init__(self, pre):
        """ Ініціалізація

        :param pre: вікно, яке визвало
        """
        self.pre = pre
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.grab_set()
        self._make_widgets()
        self._list_value = ''

    def _make_widgets(self):
        """ Сворення віджетів
        """

        _field_names = self.pre.database.get_fields('items')
        print("field names:", _field_names)

        self._entries = {}
        self._categories = sql2dict(self.pre.data_connector.get_categories())

        for el in _field_names:
            if el == 'id':
                continue

            _frame = Frame(self.diag)
            if el == 'Category_id':                                                 # список в діалоговому вікні
                el = 'Category'
                scroll_y = Scrollbar(_frame)
                scroll_y.pack(side=RIGHT, fill=Y)
                self.list_entry = Listbox(_frame, height=5,
                                  width=16, yscrollcommand=scroll_y.set)
                self.list_entry.bind('<Double-1>', self._update_text)
                _entry = Label(_frame, height=2, width=10)

                for name in self._categories.keys():
                    self.list_entry.insert(END, name)

            else:
                _entry = Entry(_frame, font=('arial', 16))

            Label(_frame, text=el + ':', font=('arial', '16')).pack(side=LEFT)

            self._entries[el] = _entry
            if el == "Category":
                self.list_entry.pack(side=RIGHT)

            _entry.pack(side=RIGHT)

            _frame.pack(side=TOP, fill=X, expand=YES)

        # кнопки
        _frame = Frame(self.diag)
        Button(_frame, text='Додати', font=('arial', '16', 'bold'),
               command=self._add_handler).pack(side=LEFT)

        Button(_frame, text='Вихід', font=('arial', '16', 'bold'),
               command=self._exit).pack(side=LEFT)
        _frame.pack(side=TOP)

    def _update_text(self, ev=None):
        entry = self._entries['Category']
        res = self.list_entry.get(self.list_entry.curselection())
        entry.configure(text=res)
        self._list_value = res
        self.diag.update()

    def _exit(self, ev=None):
        self.diag.destroy()

    def _add_handler(self, ev=None):
        """ Обробка натиснення кнопки
        """
        try:
            res = {}
            for name, entry in self._entries.items():  # зчитуємо всі поля

                if name == 'Category':
                    name = 'Category_id'
                    tmp = self._categories[self._list_value]
                else:
                    tmp = entry.get()
                if not tmp:  # якщо хоч одне поле пусте - відмова
                    return
                res[name.lower()] = tmp

            self.pre.data_connector.add_item(**res)
        except Exception as e:
            showerror(title='Error', message=e)
            print(datetime.datetime.now, ': ',  e, sep='')
