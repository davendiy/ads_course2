#!/usr/bin/env python3
# -*-encoding: utf-8-*-

""" Модуль з класами, що реалізують діалогові
вікна програми.
"""

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
import datetime
from .report import *
from docx import Document
import os


def sql2dict(dicts_list):
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {Name: id}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(Name1: id1, Name2: id2)
    """
    res = {}
    for el in dicts_list:
        res[el['Name']] = el['id']
    return res


def sql2id_dict(dicts_list):
    """ Функція, яка з списку словників (дані з бази даних) формує
    словник {id: Name}

    :param dicts_list: [dict('field1': 'val1' ... ), dict('field1': 'val1' ... )]
    :return: dict(id1: Name1, id2: Name2)
    """
    res = {}
    for el in dicts_list:
        res[el['id']] = el['Name']
    return res


class DialogEnterCategory:
    """ Діалогове вікно для додавання
    категорії товарів
    """

    def __init__(self, pre):
        self.pre = pre
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.grab_set()
        self.diag.title('Додати категорію')
        self._make_widgets()

    def _make_widgets(self):
        """ Створити віджети
        """
        # напис 'Назва категорії' і поле для введення
        _frame = Frame(self.diag)
        ttk.Label(_frame, text="Назва категорії:").pack(side=LEFT, expand=YES)
        self._entry = ttk.Entry(_frame)
        self._entry.pack(side=LEFT, expand=YES)
        _frame.pack(side=TOP, expand=YES)

        # дві кнопки
        _frame = Frame(self.diag)
        ttk.Button(_frame, text='Додати', command=self._add).pack(side=LEFT, expand=YES, padx=5, pady=5)
        ttk.Button(_frame, text='Видалити', command=self._del).pack(side=LEFT, expand=YES, padx=5, pady=5)
        _frame.pack(side=TOP)

    def _add(self, ev=None):
        """ Обробка натиснення кнопки 'Додати'

        Зчитує назву категорії і якщо це не порожній рядок - намагаєтся додати його до
        бази даних. Якщо є якась помилка - виводить відповідне вікно.
        """
        # логи
        print(datetime.datetime.now(), self.__class__, '_add', ev, '', sep='\n')
        try:
            tmp = self._entry.get()
            if tmp:
                self.pre.data_connector.add_category(tmp)
                showinfo('Success', 'Category is successfully added.')
        except Exception as exc:
            showerror('Error', exc)
            # логи
            print(datetime.datetime.now(), self.__class__, '_add', exc, sep='\n')

    def _del(self, ev=None):
        """ Обробка натиснення кнопки 'Видалити'

        Зчитує назву категорії і якщо це не порожній рядок - запитує користувача підтвердження.
        Видаляє введену категорію і всі товари цієї категорії.
        """
        # логи
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
            # логи
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

        _field_names = self.pre.database.get_fields('items')     # завантажити назви полів з таблиці 'items'

        self._entries = {}     # список полів для введення
        self._translator = sql2dict(self.pre.data_connector.get_categories())   # словник {Category_Name: Category_id}

        for el in _field_names:
            if el == 'id':                # користувач не вводить id
                continue
            _frame = Frame(self.diag)     # рамка для списку з стрічкою прокрутки (для вибору категорії
            if el == 'Category_id':       # замість введення Category_id користувач буде вибирати категорію з доступних
                el = 'Category'           # вибрана категорія відображається у відповідному написі
                scroll_y = ttk.Scrollbar(_frame)
                scroll_y.pack(side=RIGHT, fill=Y)
                self.list_entry = Listbox(_frame, height=5,
                                          width=18, yscrollcommand=scroll_y.set)
                self.list_entry.bind('<Double-1>', self._update_text)
                _entry = ttk.Label(_frame)

                for name in self._translator.keys():    # в список вставляємо всі назви категорій
                    self.list_entry.insert(END, name)

            else:  # для інших полів просто написи і поля для введення
                _entry = ttk.Entry(_frame)                      # відповідно поле для введення

            ttk.Label(_frame, text=el + ':').pack(side=LEFT)    # відповідно напис
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
        """ Заповнення напису ім'ям категорії,
        яка вибирається у списку
        """
        print(datetime.datetime.now(), self.__class__, '_update_text', ev, '\n', sep='\n')
        entry = self._entries['Category']
        res = self.list_entry.get(self.list_entry.curselection())
        entry.configure(text=res)
        self._list_value = res
        self.diag.update()

    def _exit(self, ev=None):
        """ Обробка натиснення кнопки 'Відміна'

        Просто виходить з діалогового вікна.
        """
        print(datetime.datetime.now(), self.__class__, '_exit', ev, '\n', sep='\n')
        self.diag.destroy()

    def _add_handler(self, ev=None):
        """ Обробка натиснення кнопки 'Додати'

        Зчитує інформацію з усіх полів (вони всі мають бути заповнені) і
        додає відповідний щапис у базу даних.

        Якщо виникає помилка - виводить її.
        """
        print(datetime.datetime.now(), self.__class__, '_add_handler', ev, '\n', sep='\n')
        try:
            res = {}
            for name, entry in self._entries.items():  # зчитуємо всі поля

                if name == 'Category':
                    name = 'Category_id'
                    tmp = self._translator[self._list_value]
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
    """ Діалогове вікно зміни товару.

    Викликається при подвійному натисненні на елементі списку у головному вікні.
    Поділене на 2 вкладки (ttk.Notebook).
    Дозволяє змінювати інформацію про вибраний товар + показує усі склади,
    де цей товар також наявний.

    Також забезпечує відпуск товару зі створенням накладної.
    """

    def __init__(self, pre, default: dict):
        """ Ініціалізація

        :param pre: вікно, яке визвало
        :param default: словник з інформацією про вибраний товар, яка буде виводитись
                        у полях для введення за умовчанням
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
        self._entries = {}          # словник {'Назва': 'поле для введення'}
        self._nb_frame = ttk.Frame(self.diag)
        self._nb_frame.pack(side=TOP)
        self.nb = ttk.Notebook(self._nb_frame, width=400, height=250)  # створення вкладок
        self.nb.pack()

        # додаємо 2 рамки, що стануть вкладками
        self.nbTabs = (ttk.Frame(self._nb_frame), ttk.Frame(self._nb_frame))
        self.nb.add(self.nbTabs[0], text='Змінити', padding=2)
        self.nb.add(self.nbTabs[1], text='Відпуск товару', padding=2)
        self._categories = sql2dict(self.pre.data_connector.get_categories())
        self._make_change_tab()
        self._make_product_release()

    def _make_change_tab(self):
        """ Заповнити вкладку 'Змінити' віджетами.

        Віджети такі самі, як у DialogEnterItem.
        """
        _field_names = self.pre.database.get_fields('items')    # імена полів
        print("field names:", _field_names)

        for el in _field_names:      # створення віджетів таке саме, як у DialogEnterItem,
            if el == 'id':           # тільки поля для введення заповнюються значеннями за умовчанням
                ttk.Label(self.nbTabs[0], text='Id: {}'.format(self.default[el])).pack(side=TOP)
                continue
            _frame = ttk.Frame(self.nbTabs[0])
            ttk.Label(_frame, text=el + ':').pack(side=LEFT)

            if el == 'Category_id':  # список в діалоговому вікні
                el = 'Category'
                scroll_y = ttk.Scrollbar(_frame)
                scroll_y.pack(side=RIGHT, fill=Y)
                self.list_entry = Listbox(_frame, height=5,
                                          width=18, yscrollcommand=scroll_y.set)
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

            _frame.pack()

        self._make_buttons()

    def _make_buttons(self):
        # кнопки
        _frame = Frame(self.diag)
        ttk.Button(_frame, text='Змінити',
                   command=self._change_handler).pack(side=LEFT, padx=5, pady=5)

        ttk.Button(_frame, text='Випустити',
                   command=self._release_handler).pack(side=LEFT, padx=5, pady=5)

        ttk.Button(_frame, text='Вихід',
                   command=self._exit).pack(side=LEFT, padx=5, pady=5)
        _frame.pack(side=TOP)

    def _make_product_release(self):
        """ Заповнити віджетами вкладку 'Відпуск товарів'.

        Всього 2 віджета: напис з ім'ям товару і список доступних складів.
        """
        ttk.Label(self.nbTabs[1], text=self.default['Name']).pack()

        _frame = Frame(self.nbTabs[1])   # рамка для списку з полосою прокрутки
        _frame.pack()
        scroll = Scrollbar(_frame)
        scroll.pack(side=RIGHT, fill=Y)
        listbox = Listbox(_frame, height=300, width=300, yscrollcommand=scroll.set)
        scroll.configure(command=listbox.yview)
        listbox.pack(side=RIGHT)
        # print(self.default['Name'])

        # шукаємо у базі даних елементи з таким самим ім'ям
        items = self.pre.data_connector.find_item(self.default['Name'].strip())
        print(items)
        for el in items:        # заповнення списку елементами
            string = 'Department: {},   Build: {},     Shelf: {}'
            string = string.format(el['Department_id'],
                                   el["Build_number"],
                                   el['Shelf_number'])
            listbox.insert(0, string)

    # =========================================== handlers =============================================================
    def _update_text(self, ev=None):
        """ Заповнення напису ім'ям категорії,
        яка вибирається у списку
        """
        print(datetime.datetime.now(), self.__class__, '_update_text', ev, '\n', sep='\n')
        entry = self._entries['Category']
        res = self.list_entry.get(self.list_entry.curselection())
        entry.configure(text=res)
        if res:
            self._list_value = res
        self.diag.update()

    def _exit(self, ev=None):
        """ Обробка натиснення кнопки 'Відмінити'.
        """
        print(datetime.datetime.now(), self.__class__, '_exit', ev, '\n', sep='\n')
        self.diag.destroy()

    def _release_handler(self, ev=None):
        """ Обробка натиснення кнопки 'Відпуск товару'

        Видаляє вибраний елемент (по індексу) з бази даних і ствоює накладну за шаблоном.
        """
        print(datetime.datetime.now(), self.__class__, '_release_handler', ev, '\n', sep='\n')
        try:
            self.pre.data_connector.delete_item(self.default['id'])
            outfile = asksaveasfilename(title="Зберегти накладну як...")    # запитуємо у корситувача куди зберегти

            # створюємо словник з усіма можливими полями
            # ("Name", 'id', 'Category_id', 'Category_name', 'Department_id', 'Build_number', 'Shelf_number')
            tmp_default = self.default.copy()
            tmp_default['Category'] = tmp_default['Category_id']
            tmp_default['Category_id'] = self._categories[tmp_default['Category'].strip()]

            # викликаємо відповідну функцію
            create_report(outfile, self.pre.template_invoice, [tmp_default])
            showinfo('Success', 'Одиниця товару успішно випущена. Накладна збережена до {}'.format(outfile))
            self.diag.destroy()
        except Exception as e:
            print(e)
            showerror('Error', e)

    def _change_handler(self, ev=None):
        """ Обробка натиснення кнопки 'Змінити'.

        Зчитує всю інформацію з полів для введення (усі поля мають бути заповненими) і
        записує зміни до бази даних.
        """
        print(datetime.datetime.now(), self.__class__, '_change_handler', ev, '\n', sep='\n')
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
    """ Діалог з налаштуваннями.

    Дозволяє налаштувати шлях до шаблону звіту і
    накладної та до директорії збереження звіту.
    """
    def __init__(self, pre):
        """ Ініціалізація

        :param pre: вікно, яке визвало
        """
        self.pre = pre
        self.diag = Toplevel()
        self.diag.focus_set()
        self.diag.title('Налаштування')
        self._make_widgets()

        # нові значення відповідних параметрів
        self.new_report_template = ''
        self.new_report = ''
        self.new_invoice_template = ''

    def _make_widgets(self):
        """ Сворення віджетів

        3 написи (значення відповідних параметрів), навпроти яких кнопки 'Змінити'.
        В низу вікна 2 кнопки: 'Зберегти зміни' і 'Відміна'.
        """
        self.template_label = ttk.Label(self.diag, text="Шлях до шаблону звіту: "+self.pre.template)
        ttk.Button(self.diag, text='Змінити', command=self._change_template).grid(row=1, column=3, padx=5, pady=5)
        self.template_label.grid(row=1, column=1)

        self.report_label = ttk.Label(self.diag, text="Шлях до каталогу, де буде збережено звіт: "+self.pre.report)
        ttk.Button(self.diag, text='Змінити', command=self._change_report).grid(row=3, column=3, padx=5, pady=5)
        self.report_label.grid(row=3, column=1)

        self.template_label2 = ttk.Label(self.diag, text="Шлях до шаблону накладної: " + self.pre.template_invoice)
        ttk.Button(self.diag, text='Змінити', command=self._change_template_invoice).grid(row=5, column=3,
                                                                                          padx=5, pady=5)
        self.template_label2.grid(row=5, column=1)

        ttk.Button(self.diag, text='Зберегти зміни', command=self._commit).grid(row=7, column=1)
        ttk.Button(self.diag, text='Відміна', command=self._cancel).grid(row=7, column=2, padx=5, pady=5)

    def _change_template_invoice(self, ev=None):
        """ Обробка натиснення кнопки 'Змінити' навпроти напису з
        шляхом до шаблону накладної.
        """
        print(datetime.datetime.now(), self.__class__, '_change_template_invoide', ev, '\n', sep='\n')
        new_filename = askopenfilename()  # type: str
        if new_filename:
            try:
                # намамось відкити документ як MS Word
                # (якщо неправильний документ - зініціалізується помилка)
                Document(new_filename)
                self.new_invoice_template = new_filename    # запам'ятовуємо нове значення і записуємо його до напису
                self.template_label2.config(text='Шлях до шаблону: ' + self.new_invoice_template)
            except Exception as exc:
                showerror('Error', 'Необхідно вказати MS word файл.')
                print(datetime.datetime.now(), '_change_template', exc, '', sep='\n')

    def _change_template(self, ev=None):
        """ Обробка натиснення кнопки 'Змінити' навпроти напису з
        шляхом до шаблону накладної.
        """
        print(datetime.datetime.now(), self.__class__, '_change_template', ev, '\n', sep='\n')
        new_filename = askopenfilename()   # type: str
        if new_filename:
            try:
                Document(new_filename)   # аналогічно намагаємось відкрити
                self.new_report_template = new_filename
                self.template_label.config(text='Шлях до шаблону: ' + self.new_report_template)
            except Exception as exc:
                showerror('Error', 'Необхідно вказати MS word файл.')
                print(datetime.datetime.now(), '_change_template', exc, '', sep='\n')

    def _change_report(self, ev=None):
        """ Обробка натиснення кнопки 'Змінити' навпротит напису з
        шляхом до каталогу збереження звіту
        """
        print(datetime.datetime.now(), self.__class__, '_change_report', ev, '\n', sep='\n')
        new_directory = askdirectory()  # type: str
        if new_directory:
            self.report_label.config(text='Шлях до каталогу, де буде збережено звіт: ' + new_directory)
            self.new_report = new_directory

    def _commit(self, ev=None):
        """ Обробка натиснення кнопки 'Зберегти зміни'.
        """
        print(datetime.datetime.now(), self.__class__, '_commit', ev, '\n', sep='\n')
        if self.new_report_template:
            self.pre.template = self.new_report_template
        if self.new_report:
            self.pre.report = os.path.join(self.new_report, 'report.docx')
        showinfo('Success', 'Changes saved')
        self.diag.destroy()

    def _cancel(self, ev=None):
        """ Обробка натиснення кнопки 'Відміна'
        """
        print(datetime.datetime.now(), self.__class__, '_cancel', ev, '\n', sep='\n')
        self.diag.destroy()
