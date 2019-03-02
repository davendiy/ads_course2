#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 01.03.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from tkinter.filedialog import askopenfilename
from .storage import *
from .dialogs import *


class MainWindow:

    def __init__(self, master: Tk):
        self.top = master
        self.database = None           # type: StorageDB
        self.data_connector = None     # type: StorageCollection
        self._ms_pattern = None
        self._chosen_category = ''
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
        _category_frame = Frame(_frame)
        self.input_name = Entry(_category_frame, font=('arial', '16'))
        self._category_label = Label(_category_frame, text='Вибрана категорія: ...', font=('arial', '12'))

        _list_frame = Frame(_frame)
        _scroll = Scrollbar(_list_frame)
        self.categories_list = Listbox(_list_frame, height=5, width=16, yscrollcommand=_scroll.set)
        self.categories_list.bind('<Double-1>', self._save_category)

        self._update_categories()      # наповнити кнопку вибору категорій їх списком

        _frame.pack(side=TOP, expand=1)
        _category_frame.pack(side=LEFT, expand=1)
        Label(_category_frame, text='Введіть частину назви товару:', font=('arial', '12')).pack(side=TOP,
                                                                                                fill=X, expand=1)
        self.input_name.pack(side=TOP, fill=X, expand=1)
        self._category_label.pack(side=TOP, fill=X, expand=1)

        _list_frame.pack(side=LEFT, expand=1)
        _scroll.pack(side=RIGHT, fill=Y, expand=1)
        self.categories_list.pack(side=LEFT, fill=BOTH, expand=1)
        Button(_frame, text='Шукати', font=('arial', '15'), command=self._fill_list).pack(side=RIGHT, expand=1)

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

        translator = sql2dict(self.data_connector.get_categories())
        if self._chosen_category in translator:
            tmp_val = self.data_connector.find_item(piece_name, translator[self._chosen_category])
        else:
            tmp_val = self.data_connector.find_item(piece_name)

        self.items_list.delete(0, END)
        for el in tmp_val:
            string = ''
            for field_name, val in el.items():
                if field_name == 'Category_id':
                    for name, id in translator.items():
                        if id == val:
                            val = name
                            break
                tmp = '{}: {}'.format(field_name, val)
                print(tmp, len(tmp), 30-len(tmp))
                string += '   ' + tmp + '   '
            self.items_list.insert(END, string.strip())

    def _save_category(self, ev=None):
        self._chosen_category = self.categories_list.get(self.categories_list.curselection())
        tmp = 'Вибрана категорія: ' + self._chosen_category
        print(tmp)
        self._category_label.config(text=tmp)

    def _update_categories(self):
        """ Створити список категорій для вибору у головному вікні
        """
        if self.database is not None:
            self.categories_list.delete(0, END)
            for el in self.data_connector.get_categories():
                self.categories_list.insert(END, el['Name'])
            self.categories_list.insert(END, '...')

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
