#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 01.03.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from tkinter import *
from tkinter.messagebox import showwarning
from tkinter.filedialog import askopenfilename, askdirectory
from .storage import *
from .dialogs import *


class MainWindow:

    def __init__(self, master: Tk):
        self.top = master
        self.database = None           # type: StorageDB
        self.data_connector = None     # type: StorageCollection
        self._ms_pattern = None

        self._open_database()
        self._make_widgets()

    def mainloop(self):
        self.top.mainloop()

    # ========================================= widgets ================================================================
    def _make_widgets(self):
        self.top.title("Заголовок")

        # меню
        self.menubar = Menu(self.top)
        # створити меню, що випадає, та додати до головного меню
        # tearoff=0 означає, що меню не може бути "відірване"
        # та переміщуватись у окремому вікні
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Відкрити", command=self._open_database)
        filemenu.add_separator()
        filemenu.add_command(label="Вихід", command=self.top.quit)
        self.menubar.add_cascade(label="Файл", menu=filemenu)
        # створити меню опцій
        optionsmenu = Menu(self.menubar, tearoff=0)
        optionsmenu.add_command(label="Шаблон", command=self._dialog_pattern)
        self.menubar.add_cascade(label="Опції", menu=optionsmenu)
        # показати меню
        self.top.config(menu=self.menubar)

        # рамка з полем для введення частини назви і вибору категорії
        _frame = Frame(self.top)
        self.input_name = Entry(_frame, font=('arial', '16'))
        self.categories = Menubutton(_frame, text='Категорія', relief=RAISED)
        self.input_name.pack(side=LEFT)
        self.categories.pack(side=LEFT)
        self._update_categories()      # наповнити кнопку вибору категорій їх списком
        Button(_frame, text='Шукати', font=('arial', '16'), command=self._fill_list).pack(side=LEFT)
        _frame.pack(side=TOP)

        # список - результати пошуку
        Label(self.top, text=' Результати пошуку:', font=('Helvetica', '12', 'bold')).pack(side=TOP)
        _frame = Frame(self.top)
        self.scroll_y = Scrollbar(_frame)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.items_list = Listbox(_frame, height=15,
                                  width=50, yscrollcommand=self.scroll_y.set)
        self.scroll_y.config(command=self.items_list.yview)

        self.items_list.pack(side=RIGHT, fill=BOTH, expand=YES)
        _frame.pack(side=TOP, fill=BOTH, expand=YES)
        self.items_list.bind('<Double-1>', self._change_element)

        self._fill_list()

        _frame = Frame(self.top)
        Button(_frame, text='Додати товар', font=('arial', '16'), command=self._add_item).pack(side=LEFT)
        Button(_frame, text='Додати/Видалити категорію', font=('arial', '16'),
               command=self._category_handler).pack(side=LEFT)
        Button(_frame, text='Звіт', font=('arial', '16'), command=self._create_report).pack(side=LEFT)
        _frame.pack(side=TOP, fill=X, expand=YES)

    def _fill_list(self, ev=None):
        piece_name = self.input_name.get()

        translator = sql2dict(self.data_connector.get_categories())    # TODO доробити пошук по категорії

        tmp_val = self.data_connector.find_item(piece_name)

        self.items_list.delete(0, END)
        for el in tmp_val:
            string = ' '.join('{}: {},'.format(key, value) for key, value in el.items())
            self.items_list.insert(END, string)

    def _update_categories(self):
        """ Створити список категорій для вибору у головному вікні
        """
        if self.database is not None:
            _rad_menu = Menu(self.categories)
            self.categories.configure(menu=_rad_menu)

            for el in self.data_connector.get_categories():
                _rad_menu.add_radiobutton(label=el['Name'])

    def _open_database(self):
        """ Відкрити базу даних
        """
        filename = askopenfilename()  # стандартний діалог відкриття файлу
        if filename:
            self.database = StorageDB(filename)
            self.data_connector = StorageCollection(self.database)

    def _dialog_pattern(self):
        pass

    # ================================================= handlers =======================================================
    def _add_item(self, ev=None):
        DialogEnter(self)                   # TODO додавання і видалення категорії + зміна елемента

    def _category_handler(self, ev=None):   # TODO звіт
        pass

    def _create_report(self, ev=None):
        pass

    def _change_element(self, ev=None):
        ...
