#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Модуль з класом, що реалізує головне вікно програми.
"""

from tkinter.filedialog import asksaveasfile

from .storage import *
from .dialogs import *
from .report import create_report


class MainWindow:
    """ Головне вікно програми.

    Головне вікно складається з поля для введення частини назви
    (і відповідними написами), списком з категоріями для вибору певної,
    та головним списком, в якому відображаються результати.
    """
    def __init__(self, master: Tk):
        self.top = master
        self.database = None           # type: StorageDB
        self.data_connector = None     # type: StorageCollection

        self._chosen_category = ''     # вибрана категорія
        self.template = os.path.join(os.path.curdir, 'template.docx')      # шлях до шаблону звіту
        self.report = os.path.join(os.path.curdir, 'report.docx')          # шлях збереження звіту
        self.template_invoice = os.path.join(os.path.curdir, 'template_invoice.docx')   # шлях до шаблону накладної
        tmp = 0

        # перед створенням користувачу необхідно вибрати базу даних
        # якщо він вибрав неправильний тип файлу, то дається ще спроба.
        # якщо він закрив вікно, то програма завершується.
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

        # створення меню в шапці вікна
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
        _frame = ttk.Frame(self.top)
        _category_frame = ttk.Frame(_frame)
        self.input_name = ttk.Entry(_category_frame)
        self._category_label = ttk.Label(_category_frame, text='Вибрана категорія: ...')

        # рамка з списком доступних категорій, та напису, який відображає вибрану категорію
        _list_frame = ttk.Frame(_frame)
        _scroll = ttk.Scrollbar(_list_frame)
        self.categories_list = Listbox(_list_frame, height=5, width=16, yscrollcommand=_scroll.set)
        _scroll.config(command=self.categories_list.yview)
        self.categories_list.bind('<Double-1>', self._save_category)

        self._update_categories()      # наповнити список категорій

        # пакування
        _frame.pack(side=TOP, expand=1, fill=X)
        _category_frame.grid(row=0, column=0, padx=4)
        ttk.Label(_category_frame, text='Частина назви:').pack(side=TOP,
                                                                              fill=X, expand=1)
        self.input_name.pack(side=TOP, fill=X, expand=1)
        self._category_label.pack(side=TOP, fill=X, expand=1)

        _list_frame.grid(row=0, column=2, padx=4)
        _scroll.pack(side=RIGHT, fill=Y, expand=1)
        self.categories_list.pack(side=LEFT, fill=BOTH, expand=1)
        ttk.Button(_frame, text='Шукати', command=self._fill_tree).grid(row=0, column=4, padx=5, pady=5)

        # список - результати пошуку
        tmp = ttk.Label(self.top, text=' Результати пошуку:')
        tmp.config(font=('arial', '13', 'bold'))
        tmp.pack(side=TOP)

        _frame = ttk.Frame(self.top)
        self._init_tree(_frame)
        _frame.pack(side=TOP)
        self._fill_tree()

        # кнопки
        _frame = ttk.Frame(self.top)
        ttk.Button(_frame, text='Додати товар', command=self._add_item).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(_frame, text='Додати/Видалити категорію',
                   command=self._category_handler).pack(side=LEFT, padx=5, pady=5)
        ttk.Button(_frame, text='Звіт', command=self._create_report).pack(side=LEFT, padx=5, pady=5)
        _frame.pack(side=TOP, fill=X, expand=YES)

    def _init_tree(self, pre):
        """ Створити список-дерево для відображення результатів пошуку

        :param pre: рамка, до якої прив'язана
        """
        _scroll = Scrollbar(pre)
        self.tree = ttk.Treeview(pre, yscrollcommand=_scroll.set, show='headings')
        _scroll.config(comman=self.tree.yview)
        _scroll.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=RIGHT)
        self.tree['columns'] = ROWS_MAIN
        self.tree.bind('<Double-1>', self._change_element)
        for el in ROWS_MAIN:
            self.tree.column(el, width=120, anchor='center')
            self.tree.heading(el, text=el, anchor='center')

    def _fill_tree(self, ev=None):
        """ Обробити подвійне натиснення на елемент списку.

        Заповнити список-дерево елементами з результатів пошуку.
        """
        print(datetime.datetime.now(), '_fill_tree', ev, sep='\n')
        piece_name = self.input_name.get()      # частина назви
        translator1 = name_dict(self.data_connector.get_categories())     # dict("Name": "id")
        translator2 = id_dict(self.data_connector.get_categories())  # dict("id": "Name")

        # якщо категорія вибрана - пошук по частині назви і категорії
        if self._chosen_category in translator1:
            tmp_val = self.data_connector.find_item(piece_name, translator1[self._chosen_category])
        else:      # інакше - по частині імені
            tmp_val = self.data_connector.find_item(piece_name)

        # видаляємо всі елементи і заповнюємо наново
        self.tree.delete(*self.tree.get_children())
        for el in tmp_val:
            el['Category'] = translator2[el['Category_id']]
            del el["Category_id"]
            tmp = tuple(map(lambda a: el[a], ROWS_MAIN))
            self.tree.insert("", 'end', text='', values=tmp)

    def _update_categories(self):
        """ Створити список категорій для вибору у головному вікні
        """
        if self.database is not None:
            self.categories_list.delete(0, END)
            for el in self.data_connector.get_categories():
                self.categories_list.insert(END, el['Name'])
            self.categories_list.insert(END, '...')

    # ========================================= handlers ===============================================================
    def _save_category(self, ev=None):
        """ Обробка подвійного натиснення на елемент списку категорій

        Зберігає вибрану категорію у відповідній змінній
        та перезаписує напис з вибраною категорією.
        """
        print(datetime.datetime.now(), '_save_category', ev, sep='\n')
        self._chosen_category = self.categories_list.get(self.categories_list.curselection())
        tmp = 'Вибрана категорія: ' + self._chosen_category
        # print(tmp)
        self._category_label.config(text=tmp)

    def _open_database(self):
        """ Відкрити базу даних

        Викликається з самого початку + після натиснення відповідної кнопки в меню.
        """
        filename = askopenfilename()  # стандартний діалог відкриття файлу
        if filename:
            try:
                database = StorageDB(filename)          # пробуємо підключитись до бази даних
                data_connector = StorageCollection(database)   # якщо щось піде не так - зініціюється виключення
                data_connector.get_categories()

                self.database = database  # якщо все пройшло нормально - змінюємо об'єкти StorageDB i StorageCollection
                self.data_connector = data_connector
                return 1                  # 1 - все нормально
            except Exception as exc:
                showerror("Error", "Необхідно вибрати базу даних.")
                print(datetime.datetime.now(), '_open_database', exc, '\n', sep='\n')
                return 0                  # 0 - дати ще один шанс
        return 2                          # 2 - закрити вікно і вийти з програми, якщо це відбувається вперше

    def _add_item(self, ev=None):
        """ Обробка натиснення кнопки 'Додати товар'.

        Викликає відповідне діалогове вікно. Після його завершення оновлює всі дані.
        """
        print(datetime.datetime.now(), '_add_item', ev, '\n', sep='\n')
        tmp = DialogEnterItem(self)
        self.top.wait_window(tmp.diag)
        self._update_categories()
        self._chosen_category = ''
        self.input_name.clipboard_clear()
        self._category_label.config(text='Вибрана категорія: ...')
        self._fill_tree()

    def _category_handler(self, ev=None):
        """ Обробка натиснення кнопки 'Додати/Видалити категорію'.

        Викликає відповідне діалогове вікно. Після його завершення оновлює всі дані.
        """
        print(datetime.datetime.now(), '_category_handler', ev, '\n', sep='\n')
        tmp = DialogAddCategory(self)
        self.top.wait_window(tmp.diag)
        self._update_categories()
        self._chosen_category = ''
        self.input_name.clipboard_clear()
        self._category_label.config(text='Вибрана категорія: ...')
        self._fill_tree()

    def _create_report(self, ev=None):
        """ Обробляє натиснення кнопки 'Звіт'

        Формує список словників з інформацією з бази даних і викликає відповідну
        функцію для створення звіту за шаблоном.
        """
        print(datetime.datetime.now(), '_create_report', ev, '\n', sep='\n')
        try:
            all_data = self.data_connector.get_items()
            categories = id_dict(self.data_connector.get_categories())
            for row in all_data:
                row['Category'] = categories[row['Category_id']]
            create_report(self.report, self.template, all_data)
            showinfo('Success', "Report is successfully created into {}".format(self.report))
        except Exception as exc:
            print(datetime.datetime.now(), '_create_report', exc, '', sep='\n')
            showerror("Error", exc)

    def _change_element(self, ev=None):
        """ Обробка подвійного натиснення на елемент списку.

        Викликає відповідне діалогове вікно (Змінити елемент), після
        його завершення оновлює інформацію в головному вікні.
        """
        print(datetime.datetime.now(), '_change_element', ev, '\n', sep='\n')
        translator = name_dict(self.data_connector.get_categories())
        default = self.tree.focus()
        default = self.tree.item(default)

        default = dict(zip(ROWS_DIALOG, default['values']))
        default['Category_id'] = translator[default['Category']]
        del default["Category"]
        tmp = DialogChangeItem(self, default)
        self.top.wait_window(tmp.diag)
        self._update_categories()
        self._chosen_category = ''
        self.input_name.clipboard_clear()
        self._category_label.config(text='Вибрана категорія: ...')
        self._fill_tree()

    def _settings(self):
        """ Обробка подвійного натиснення на 'Налаштування'

        Викликає відповідне діалогове вікно, після
        його завершення оновлює інформацію в головному вікні.
        """
        print(datetime.datetime.now(), '_settings', '\n', sep='\n')
        tmp = DialogSettings(self)
        self.top.wait_window(tmp.diag)
        self._update_categories()

    def _save_database(self):
        """ Обробка натиснення 'Зберегти як'.

        Зберігає базу даних у вказаний файл.
        """
        fileout = asksaveasfile(mode='wb')
        if fileout:
            filein = open(self.database.urn, 'rb')
            try:
                # копіюємо інформацію порціями, щоб не було переповнення буферу.
                for i in range(os.path.getsize(self.database.urn) // CHUNK + 1):
                    fileout.write(filein.read(CHUNK))
            except Exception as exc:
                print(datetime.datetime.now(), '_save_database:', exc, '', sep='\n')
                filein.close()
                fileout.close()
