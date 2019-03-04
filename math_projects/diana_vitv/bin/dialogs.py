#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter.filedialog import askopenfilename, askdirectory
import datetime
from docx import Document
import os
# from .main_window import MainWindow


def sql2dict(dicts_list):
    res = {}
    for el in dicts_list:
        res[el['Name']] = el['id']
    return res


def sql2id_dict(dicts_list):
    res = {}
    for el in dicts_list:
        res[el['id']] = el['Name']
    return res


class DialogEnterCategory:

    def __init__(self, pre):
        self.pre = pre
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.grab_set()
        self._make_widgets()

    def _make_widgets(self):
        _frame = Frame(self.diag)
        ttk.Label(_frame, text="Назва категорії:").pack(side=LEFT, expand=YES)
        self._entry = ttk.Entry(_frame)
        self._entry.pack(side=LEFT, expand=YES)
        _frame.pack(side=TOP, expand=YES)

        _frame = Frame(self.diag)
        ttk.Button(_frame, text='Додати', command=self._add).pack(side=LEFT, expand=YES, padx=5, pady=5)
        ttk.Button(_frame, text='Видалити', command=self._del).pack(side=LEFT, expand=YES, padx=5, pady=5)
        _frame.pack(side=TOP)

    def _add(self, ev=None):
        print(datetime.datetime.now(), self.__class__, '_add', ev, '', sep='\n')
        try:
            tmp = self._entry.get()
            if tmp:
                self.pre.data_connector.add_category(tmp)
                showinfo('Success', 'Category is successfully added.')
        except Exception as exc:
            showerror('Error', exc)
            print(datetime.datetime.now(), self.__class__, '_add', exc, sep='\n')

    def _del(self, ev=None):
        print(datetime.datetime.now(), self.__class__, '_del', ev, '', sep='\n')
        try:
            tmp = self._entry.get()
            if tmp:
                ans = askokcancel('Увага', 'Видалення категорії призведе '
                                           'до видалення всіх товарів даної категорії.'
                                           'Бажаєте продовжити?')
                if ans:
                    self.pre.data_connector.delete_category(tmp)
                    showinfo('Success', 'Category is successfully deleted.')
        except Exception as e:
            showerror('Error', e)
            print(datetime.datetime.now(), self.__class__, '_del', e, sep='\n')


class DialogEnterItem:
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
        self.diag.title('Додати одиницю товару')
        self._make_widgets()
        self._list_value = ''

    def _make_widgets(self):
        """ Сворення віджетів
        """

        _field_names = self.pre.database.get_fields('items')
        # print("field names:", _field_names)

        self._entries = {}
        self._categories = sql2dict(self.pre.data_connector.get_categories())

        for el in _field_names:
            if el == 'id':
                continue

            _frame = Frame(self.diag)
            if el == 'Category_id':  # список в діалоговому вікні
                el = 'Category'
                scroll_y = ttk.Scrollbar(_frame)
                scroll_y.pack(side=RIGHT, fill=Y)
                self.list_entry = Listbox(_frame, height=5,
                                          width=16, yscrollcommand=scroll_y.set)
                self.list_entry.bind('<Double-1>', self._update_text)
                _entry = ttk.Label(_frame)

                for name in self._categories.keys():
                    self.list_entry.insert(END, name)

            else:
                _entry = ttk.Entry(_frame)

            ttk.Label(_frame, text=el + ':').pack(side=LEFT)

            self._entries[el] = _entry
            if el == "Category":
                self.list_entry.pack(side=RIGHT)

            _entry.pack(side=RIGHT)

            _frame.pack(side=TOP, fill=X, expand=YES)

        # кнопки
        _frame = Frame(self.diag)
        ttk.Button(_frame, text='Додати',
                   command=self._add_handler).pack(side=LEFT, padx=5, pady=5)

        ttk.Button(_frame, text='Вихід',
                   command=self._exit).pack(side=LEFT, padx=5, pady=5)
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
            showinfo('Success', 'New item is successfully added')

        except Exception as e:
            showerror(title='Error', message=e)
            print(datetime.datetime.now, ': ', e, sep='')


class DialogChangeItem:

    def __init__(self, pre, default: dict):
        """ Ініціалізація

        :param pre: вікно, яке визвало
        """
        self.pre = pre
        self.diag = Toplevel()
        self.diag.focus_set()
        self.default = default
        self.diag.title('Змінити одиницю товару')
        self._make_widgets()
        self._list_value = default['Category_id']

    def _make_widgets(self):
        """ Сворення віджетів
        """

        _field_names = self.pre.database.get_fields('items')
        print("field names:", _field_names)

        self._entries = {}
        self._categories = sql2dict(self.pre.data_connector.get_categories())

        for el in _field_names:
            if el == 'id':
                ttk.Label(self.diag, text='Id: {}'.format(self.default[el])).pack(side=TOP)
                continue
            _frame = Frame(self.diag)
            ttk.Label(_frame, text=el + ':').pack(side=LEFT)

            if el == 'Category_id':  # список в діалоговому вікні
                el = 'Category'
                scroll_y = ttk.Scrollbar(_frame)
                scroll_y.pack(side=RIGHT, fill=Y)
                self.list_entry = Listbox(_frame, height=5,
                                          width=16, yscrollcommand=scroll_y.set)
                self.list_entry.bind('<Double-1>', self._update_text)
                _entry = ttk.Label(_frame, text=self.default['Category_id'])
                self._list_value = self.default['Category_id']

                for name in self._categories.keys():
                    self.list_entry.insert(END, name)

            else:
                _entry = ttk.Entry(_frame)
                _entry.insert(0, self.default[el])

            self._entries[el] = _entry
            if el == "Category":
                self.list_entry.pack(side=RIGHT)

            _entry.pack(side=RIGHT)

            _frame.pack(side=TOP, fill=X, expand=YES)

        # кнопки
        _frame = Frame(self.diag)
        ttk.Button(_frame, text='Змінити',
                   command=self._change_handler).pack(side=LEFT, padx=5, pady=5)

        ttk.Button(_frame, text='Видалити',
                   command=self._del_handler).pack(side=LEFT, padx=5, pady=5)

        ttk.Button(_frame, text='Вихід',
                   command=self._exit).pack(side=LEFT, padx=5, pady=5)
        _frame.pack(side=TOP)

    def _update_text(self, ev=None):
        entry = self._entries['Category']
        res = self.list_entry.get(self.list_entry.curselection())
        entry.configure(text=res)
        if res:
            self._list_value = res
        self.diag.update()

    def _exit(self, ev=None):
        self.diag.destroy()

    def _del_handler(self, ev=None):
        try:
            ans = askokcancel(title='Увага',
                              message='Ви впевнені, що хочете видалити одиницю товару {}?'.format(self.default['Name']))
            if ans:
                self.pre.data_connector.delete_item(self.default['id'])
                showinfo('Success', 'Одиниця товару успішно видалена.')
                self.diag.destroy()
        except Exception as e:
            print(e)
            showerror('Error', e)

    def _change_handler(self, ev=None):
        """ Обробка натиснення кнопки
        """
        try:
            res = {}
            for name, entry in self._entries.items():  # зчитуємо всі поля

                if name == 'Category':
                    name = 'Category_id'
                    tmp = self._categories[self._list_value.strip()]
                else:
                    tmp = entry.get()
                if not tmp:  # якщо хоч одне поле пусте - відмова
                    return
                res[name.lower()] = tmp
            res['item_id'] = self.default['id']
            ans = askokcancel('Увага', 'Ви дійсно хочете змінити елемент (скасувати дію буде неможливо)?')
            if ans:
                self.pre.data_connector.change_item(**res)
                showinfo('Success', 'Item is successfully changed')
                self.diag.destroy()

        except Exception as e:
            showerror(title='Error', message=e)
            print(datetime.datetime.now, ': ', e, sep='')


class DialogSettings:

    def __init__(self, pre):
        """ Ініціалізація

        :param pre: вікно, яке визвало
        """
        self.pre = pre
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.title('Налаштування створення звіту')
        self._make_widgets()
        self.new_template = ''
        self.new_report = ''

    def _make_widgets(self):
        """ Сворення віджетів
        """

        self.template_label = ttk.Label(self.diag, text="Шлях до шаблону: "+self.pre.template)
        ttk.Button(self.diag, text='Змінити', command=self._change_template).grid(row=1, column=3, padx=5, pady=5)
        self.template_label.grid(row=1, column=1)

        self.report_label = ttk.Label(self.diag, text="Шлях до каталогу, де буде збережено звіт: "+self.pre.report)
        ttk.Button(self.diag, text='Змінити', command=self._change_report).grid(row=3, column=3, padx=5, pady=5)
        self.report_label.grid(row=3, column=1)

        ttk.Button(self.diag, text='Зберегти зміни', command=self._commit).grid(row=5, column=1)
        ttk.Button(self.diag, text='Відміна', command=self._cancel).grid(row=5, column=2, padx=5, pady=5)

    def _change_template(self, ev=None):
        new_filename = askopenfilename()   # type: str
        if new_filename:
            try:
                Document(new_filename)
                self.new_template = new_filename
                self.template_label.config(text='Шлях до шаблону: '+ self.new_template)
            except Exception as exc:
                showerror('Error', 'Необхідно вказати MS word файл.')
                print(datetime.datetime.now(), '_change_template', exc, '', sep='\n')

    def _change_report(self, ev=None):
        new_directory = askdirectory()  # type: str
        if new_directory:
            self.report_label.config(text='Шлях до каталогу, де буде збережено звіт: ' + new_directory)
            self.new_report = new_directory

    def _commit(self, ev=None):
        if self.new_template:
            self.pre.template = self.new_template
        if self.new_report:
            self.pre.report = os.path.join(self.new_report, 'report.docx')
        showinfo('Success', 'Changes saved')
        self.diag.destroy()

    def _cancel(self, ev=None):
        self.diag.destroy()
