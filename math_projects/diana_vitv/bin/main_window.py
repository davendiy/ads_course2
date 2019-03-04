#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter.filedialog import asksaveasfile
from .storage import *
from .dialogs import *
from .report import create_report
import os
import datetime

# TODO додати відпуск товару (ідентичний видаленню)

CHUNK = 1024 * 100


class MainWindow:

    def __init__(self, master: Tk):
        self.top = master
        self.database = None           # type: StorageDB
        self.data_connector = None     # type: StorageCollection
        self._ms_pattern = None
        self._chosen_category = ''
        self.template = os.path.join(os.path.curdir, 'template.docx')
        self.report = os.path.join(os.path.curdir, 'report.docx')
        tmp = 0
        while tmp != 1:
            tmp = self._open_database()
            if tmp == 2:
                self.top.destroy()
                break
        if tmp == 1:
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
        filemenu.add_command(label="Зберегти як", command=self._save_database)
        filemenu.add_separator()
        filemenu.add_command(label="Вихід", command=self.top.quit)
        self.menubar.add_cascade(label="Файл", menu=filemenu)
        # створити меню опцій
        optionsmenu = Menu(self.menubar, tearoff=0)
        optionsmenu.add_command(label="Параметри створення звіту", command=self._settings)
        self.menubar.add_cascade(label="Опції", menu=optionsmenu)
        # показати меню
        self.top.config(menu=self.menubar)

        # рамка з полем для введення частини назви і вибору категорії
        _frame = Frame(self.top)
        _category_frame = Frame(_frame)
        self.input_name = ttk.Entry(_category_frame)
        self._category_label = ttk.Label(_category_frame, text='Вибрана категорія: ...')

        _list_frame = Frame(_frame)
        _scroll = ttk.Scrollbar(_list_frame)
        self.categories_list = Listbox(_list_frame, height=5, width=16, yscrollcommand=_scroll.set)
        self.categories_list.bind('<Double-1>', self._save_category)

        self._update_categories()      # наповнити кнопку вибору категорій їх списком

        _frame.pack(side=TOP, expand=1)
        _category_frame.grid(row=0, column=0, padx=4)
        ttk.Label(_category_frame, text='Введіть частину назви товару:').pack(side=TOP,
                                                                              fill=X, expand=1)
        self.input_name.pack(side=TOP, fill=X, expand=1)
        self._category_label.pack(side=TOP, fill=X, expand=1)

        _list_frame.grid(row=0, column=2, padx=4)
        _scroll.pack(side=RIGHT, fill=Y, expand=1)
        self.categories_list.pack(side=LEFT, fill=BOTH, expand=1)
        ttk.Button(_frame, text='Шукати', command=self._fill_list).grid(row=0, column=4, padx=4)

        # список - результати пошуку
        ttk.Label(self.top, text=' Результати пошуку:').pack(side=TOP)
        _frame = Frame(self.top)
        self.scroll_y = ttk.Scrollbar(_frame)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.items_list = Listbox(_frame, height=15,
                                  width=50, yscrollcommand=self.scroll_y.set)
        self.scroll_y.config(command=self.items_list.yview)

        self.items_list.pack(side=RIGHT, fill=BOTH, expand=YES)
        _frame.pack(side=TOP, fill=BOTH, expand=YES)
        self.items_list.bind('<Double-1>', self._change_element)

        self._fill_list()

        _frame = Frame(self.top)
        ttk.Button(_frame, text='Додати товар', command=self._add_item).pack(side=LEFT)
        ttk.Button(_frame, text='Додати/Видалити категорію',
                   command=self._category_handler).pack(side=LEFT)
        ttk.Button(_frame, text='Звіт', command=self._create_report).pack(side=LEFT)
        _frame.pack(side=TOP, fill=X, expand=YES)

    def _fill_list(self, ev=None):
        print(datetime.datetime.now(), '_fill_list', ev, '', sep='\n')
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
                    for name, _id in translator.items():
                        if _id == val:
                            val = name
                            break
                tmp = '{}: {}'.format(field_name, val)
                # print(tmp, len(tmp), 30-len(tmp))
                string += '   ' + tmp + '   '
            self.items_list.insert(END, string.strip())

    def _update_categories(self):
        """ Створити список категорій для вибору у головному вікні
        """
        if self.database is not None:
            self.categories_list.delete(0, END)
            for el in self.data_connector.get_categories():
                self.categories_list.insert(END, el['Name'])
            self.categories_list.insert(END, '...')

    # ========================================= handlers ===============================================================
    def _dialog_pattern(self):
        pass

    def _save_category(self, ev=None):
        print(datetime.datetime.now(), '_save_category', ev, sep='\n')
        self._chosen_category = self.categories_list.get(self.categories_list.curselection())
        tmp = 'Вибрана категорія: ' + self._chosen_category
        # print(tmp)
        self._category_label.config(text=tmp)

    def _open_database(self):
        """ Відкрити базу даних
        """
        filename = askopenfilename()  # стандартний діалог відкриття файлу
        if filename:
            try:
                database = StorageDB(filename)
                data_connector = StorageCollection(database)
                data_connector.get_categories()

                self.database = database
                self.data_connector = data_connector
                return 1
            except Exception as exc:
                showerror("Error", "Необхідно вибрати базу даних.")
                print(datetime.datetime.now(), '_open_database', exc, '\n', sep='\n')
                return 0
        return 2

    def _add_item(self, ev=None):
        print(datetime.datetime.now(), '_add_item', ev, '\n', sep='\n')
        tmp = DialogEnterItem(self)
        self.top.wait_window(tmp.diag)
        self._update_categories()
        self._chosen_category = ''
        self.input_name.clipboard_clear()
        self._category_label.config(text='Вибрана категорія: ...')
        self._fill_list()

    def _category_handler(self, ev=None):
        print(datetime.datetime.now(), '_category_handler', ev, '\n', sep='\n')
        tmp = DialogEnterCategory(self)
        self.top.wait_window(tmp.diag)
        self._update_categories()
        self._chosen_category = ''
        self.input_name.clipboard_clear()
        self._category_label.config(text='Вибрана категорія: ...')
        self._fill_list()

    def _create_report(self, ev=None):
        print(datetime.datetime.now(), '_create_report', ev, '\n', sep='\n')
        try:
            all_data = self.data_connector.get_items()
            categories = sql2id_dict(self.data_connector.get_categories())
            for row in all_data:
                row['Category'] = categories[row['Category_id']]
            create_report(self.report, self.template, all_data)
            showinfo('Success', "Report is successfully created into {}".format(self.report))
        except Exception as exc:
            print(datetime.datetime.now(), '_create_report', exc, '', sep='\n')
            showerror("Error", exc)

    def _change_element(self, ev=None):
        print(datetime.datetime.now(), '_change_element', ev, '\n', sep='\n')
        default = self.items_list.get(self.items_list.curselection())
        default = dict(map(lambda a: a.split(":"), default.split('      ')))
        tmp = DialogChangeItem(self, default)
        self.top.wait_window(tmp.diag)
        self._update_categories()
        self._chosen_category = ''
        self.input_name.clipboard_clear()
        self._category_label.config(text='Вибрана категорія: ...')
        self._fill_list()

    def _settings(self):
        print(datetime.datetime.now(), '_settings', '\n', sep='\n')
        tmp = DialogSettings(self)
        self.top.wait_window(tmp.diag)
        self._update_categories()

    def _save_database(self):
        fileout = asksaveasfile(mode='wb')
        if fileout:
            filein = open(self.database.urn, 'rb')
            try:
                for i in range(os.path.getsize(self.database.urn) // CHUNK + 1):
                    fileout.write(filein.read(CHUNK))
            except Exception as exc:
                print(datetime.datetime.now(), '_save_database:', exc, '', sep='\n')
                filein.close()
                fileout.close()
