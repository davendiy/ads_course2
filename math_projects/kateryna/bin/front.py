#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning, askyesno, showinfo, showerror
from tkinter.filedialog import asksaveasfilename
from webbrowser import open

from .client import *
from .database import *
from .constants import *

now_date = datetime.datetime.now().date()


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self._dialog_category = ''
        self._make_widgets()

    def _make_widgets(self):
        """ Створити віджети
        """
        self.title('MonitorGui')  # заголовок

        # --------------------------------Menu-----------------------------------------
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Save as", command=self._save_database)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        optionsmenu = Menu(self.menubar, tearoff=0)
        optionsmenu.add_command(label="Monitor now", command=self._monitor)
        self.menubar.add_cascade(label="Monitoring", menu=optionsmenu)
        self.config(menu=self.menubar)

        # -------------------------------Tabs-----------------------------------------
        self._nb_frame = ttk.Frame(self)
        self._nb_frame.pack(side=TOP)
        self.nb = ttk.Notebook(self._nb_frame, height=340)
        self.nb.pack(padx=5)
        self.nbTabs = tuple([ttk.Frame(self._nb_frame) for _ in range(2)])
        self.nb.add(self.nbTabs[0], text='Monitoring', padding=2)
        self.nb.add(self.nbTabs[1], text='Settings', padding=2)

        self._make_general_tab(self.nbTabs[0])
        self._make_settings_tab(self.nbTabs[1])

    def _make_general_tab(self, main_frame):
        """ Заповнити віджетами вкладку Monitoring

        :param main_frame: рамка, на якій треба все розміщувати
        """
        # --------------------------Top Buttons---------------------------------------

        ttk.Label(main_frame, text='From:').grid(row=1, column=1, padx=5, pady=5)
        self._date_from = ttk.Entry(main_frame, width=12)
        self._date_from.insert(0, '1950-01-01')
        self._date_from.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(main_frame, text='To:').grid(row=1, column=3, padx=5, pady=5)
        self._date_to = ttk.Entry(main_frame, width=12)
        self._date_to.grid(row=1, column=4, padx=5, pady=5)
        self._date_to.insert(0, str(now_date))

        ttk.Button(main_frame, text='Update', command=self._fill_monitor_tree).grid(row=1, column=6, padx=5, pady=5)

        # -------------------------OptionMenu------------------------------------
        self._gen_chosen_category = StringVar(main_frame)
        categories = id_dict(database.get_categories())
        option_menu = ttk.OptionMenu(main_frame, self._gen_chosen_category, '...', *categories.values(), '...')
        option_menu.config(width=17)
        option_menu.grid(row=1, column=5, padx=5, pady=5)

        # --------------------------TreeView--------------------------------------
        _frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(_frame)
        self._monitor_tree = ttk.Treeview(_frame, show='headings', yscrollcommand=scroll.set, height=14)
        scroll.config(command=self._monitor_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self._monitor_tree['columns'] = LINKS_GUI_FIELDS
        self._monitor_tree.pack(side=RIGHT)
        for el in LINKS_GUI_FIELDS:
            self._monitor_tree.column(el, width=180, anchor='center')
            self._monitor_tree.heading(el, text=el, anchor='center')

        self._monitor_tree.bind('<Double-1>', self._run_browser)
        _frame.grid(row=2, column=1, columnspan=6)
        self._fill_monitor_tree()

    def _fill_monitor_tree(self, ev=None):
        """ Наповнити деревовидний список інформацією з БД
        """
        tmp = self._gen_chosen_category.get()    # вибрана категорія
        if self._date_from.get():
            try:
                date_from = list(map(int, self._date_from.get().split('-')))   # намагаємось зчитати введену дату
                date_to = list(map(int, self._date_to.get().split('-')))
                date_from = datetime.datetime(*date_from)
                date_to = datetime.datetime(*date_to)
            except Exception as e:
                showerror('Error', 'Please, enter the correct date in format yyyy-mm-dd.')
                logging.exception(e)
                return
        else:
            date_from = datetime.datetime.min    # якщо дата пуста - беремо дані за умовчанням
            date_to = datetime.datetime.max

        tmp = database.get_category_id(tmp)      # знаходимо ідентифікатор вибраної категорії
        items = database.get_items(item_type=LINK, category=tmp)       # знаходимо елементи вибраної категорії
        self._monitor_tree.delete(*self._monitor_tree.get_children())  # видаляємо попередні значення

        # словник {"Category_name": "Category_id"}
        translator = id_dict(database.get_categories())

        # виводимо елементи, які входять у вибраний часовий період
        for el in items:
            el['Category'] = translator[el['Category_id']]  # замість ідентифікатора відобржаємо назву катеорій
            del el['Category_id']

            el['Date'] = el['Date'][:el['Date'].rindex('.')]    # видаляємо знаки після коми секунд
            tmp_date = datetime.datetime(*map(int, el['Date'].split()[0].split('-')))
            if not date_from <= tmp_date <= date_to:            # якщо не входить у часовий період - пропускаємо
                continue
            # формуємо список необхідних значень, які треба заповнити
            tmp = tuple(map(lambda a: el[a], LINKS_GUI_FIELDS))
            self._monitor_tree.insert('', 0, text='', values=tmp)

    def _make_settings_tab(self, main_frame):
        """ Наповнити віджетами вкладку Settings

        :param main_frame: рамка, на якій треба все розміщувати
        """
        # -------------------------------First row----------------------------------------------------------------------
        self._set_chosen_category = StringVar(main_frame)  # змінна, яка пов'язана з випадаючим меню вибору категорії

        # словник {"Category_id":"Category_name"}
        categories = id_dict(database.get_categories())
        # якщо категорія не вибрана (тобто вкладка формується перший раз), то вибираємо першу категорію
        chosen_cat = '' if not categories else next(iter(categories.values()))
        option_menu = ttk.OptionMenu(main_frame, self._set_chosen_category, chosen_cat, *categories.values())
        option_menu.config(width=20)
        option_menu.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(main_frame, text='Delete category', command=self._delete_category).grid(row=1,
                                                                                           column=2,
                                                                                           padx=5,
                                                                                           pady=5)

        ttk.Button(main_frame, text="Update", command=self._fill_settings).grid(row=1, column=3, padx=5, pady=5)

        # -------------------------------Second row (TreeView)----------------------------------------------------------
        _frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(_frame)
        self._sites_tree = ttk.Treeview(_frame, show='headings', yscrollcommand=scroll.set, height=4)
        scroll.config(command=self._sites_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self._sites_tree['columns'] = SITES_GUI_FIELDS
        self._sites_tree.pack(side=RIGHT)

        self._sites_tree.column("Id", width=80, anchor='center')
        self._sites_tree.heading('Id', text="Id", anchor='center')

        self._sites_tree.column("Name", width=180, anchor='center')
        self._sites_tree.heading('Name', text="Name", anchor='center')

        self._sites_tree.column("Link", width=300, anchor='center')
        self._sites_tree.heading('Link', text="Link", anchor='center')

        self._sites_tree.bind('<Double-1>', self._change_site)
        _frame.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

        # ------------------------------Third row (Button and Entries)--------------------------------------------------
        self._site_name = ttk.Entry(main_frame)
        self._site_name.grid(row=3, column=1, padx=5, pady=5)
        self._site_name.insert(0, 'Name')
        self._site_url = ttk.Entry(main_frame)
        self._site_url.grid(row=3, column=2, padx=5, pady=5)
        self._site_url.insert(0, 'http://www.link.com')
        ttk.Button(main_frame, text='Add', command=self._add_site).grid(row=3, column=3, padx=5, pady=5)

        # ------------------------------Fourth row (TreeView)-----------------------------------------------------------
        _frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(_frame)
        self._words_tree = ttk.Treeview(_frame, show='headings', yscrollcommand=scroll.set, height=4)
        scroll.config(command=self._words_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self._words_tree['columns'] = KEY_WORDS_GUI_FIELDS
        self._words_tree.pack(side=RIGHT)

        self._words_tree.column("Id", width=80, anchor='center')
        self._words_tree.heading("Id", text="Id", anchor='center')

        self._words_tree.column("Word", width=480, anchor='center')
        self._words_tree.heading('Word', text="Word", anchor='center')

        self._words_tree.bind('<Double-1>', self._change_word)
        _frame.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

        self._fill_settings()

        # ------------------------------Fifth row (Buttons and Entry)---------------------------------------------------
        self._word = ttk.Entry(main_frame)
        self._word.grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text='Add', command=self._add_word).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(main_frame, text='New category', command=self._add_category).grid(row=5, column=3, padx=5, pady=5)

    # =========================================HANDLERS=================================================================
    def _run_browser(self, ev=None):
        """ За подвійним натисненням на елемент деревовидного списку на
        вкладці Monitoring відкриваємо адресу вибраного елемена у браузері
        """
        item = self._monitor_tree.focus()
        params = dict(zip(LINKS_GUI_FIELDS, self._monitor_tree.item(item)['values']))
        open(params['Link'])

    def _change_site(self, ev=None):
        """ Подвійне натиснення на елемент деревовидного списку на вкладці Settings викликає
        діалогове вікно зміни відповідного елемента. В данову випадку
        змінюється сайт.
        """
        item = self._sites_tree.focus()
        _default = dict(zip(SITES_GUI_FIELDS, self._sites_tree.item(item)['values']))
        tmp = DialogChangeSite(_default, item_type=SITE)
        tmp.diag.wait_window()
        self._fill_settings()

    def _change_word(self, ev=None):
        """ Подвійне натиснення на елемент деревовидного списку на вкладці Settings викликає
        діалогове вікно зміни відповідного елемента. В даному випадку змінюється ключове слово.
        """
        item = self._words_tree.focus()
        _default = dict(zip(KEY_WORDS_GUI_FIELDS, self._words_tree.item(item)['values']))
        tmp = DialogChangeSite(_default, item_type=KEY_WORD)
        tmp.diag.wait_window()
        self._fill_settings()

    def _fill_settings(self, ev=None):
        """ Наповнити списки на вкладці Settings.

        Викликається при натисненні на кнопку Update
        """
        category = self._set_chosen_category.get()
        category = database.get_category_id(category)

        self._sites_tree.delete(*self._sites_tree.get_children())  # видаляємо попередні значення
        self._words_tree.delete(*self._words_tree.get_children())

        # шукаємо в БД елементи з відповідними параметрами і заповнюємо обидва списка
        items = database.get_items(item_type=SITE, category=category)
        for el in items:
            tmp = tuple(map(lambda a: el[a], SITES_GUI_FIELDS))
            self._sites_tree.insert('', 0, text='', values=tmp)

        items = database.get_items(item_type=KEY_WORD, category=category)
        for el in items:
            tmp = tuple(map(lambda a: el[a], KEY_WORDS_GUI_FIELDS))
            self._words_tree.insert('', 0, text='', values=tmp)

    def _add_word(self, ev=None):
        """ Обробити натиснення кнопки Add під списком Words

        Зчитуємо значення з полів для введення, додаємо в БД і оновлюємо списки.
        """
        word = self._word.get()
        if word:
            category = self._set_chosen_category.get()
            category = database.get_category_id(category)
            database.add_item(item_type=KEY_WORD, Word=word, Category_id=category)
            self._fill_settings()

    def _add_site(self, ev=None):
        """ Обробити натиснення кнопки Add під списком Sites

        Зчитуємо значення з полів для введення, додаємо в БД і оновлюємо списки.
        """
        name = self._site_name.get()
        link = self._site_url.get()

        try:
            urlopen(link)     # намагаємось підключитись до введеного сайту
        except HTTPError:
            # якщо не вдається  підключитись - виводимо попередження
            showwarning('Warning', "Couldn't open {}".format(link))
        except Exception as e:
            showerror('Error', 'Please, enter the correct url')  # якщо проблема в адресі - виводимо помилку
            logging.exception(e)
            return

        if name and link:   # якщо обидва поля не пусті - додаємо до БД і оновлюємо
            category = self._set_chosen_category.get()
            category = database.get_category_id(category)
            database.add_item(item_type=SITE, Name=name, Link=link, Category_id=category)
            self._fill_settings()

    def _delete_category(self, ev=None):
        """ Видалити категорію і всі записи, пов'язані з нею
        """
        if askyesno('Warning', 'Do you really want to delete this category (all the results of '
                               'monitoring for this category will be deleted)?'):
            category = self._set_chosen_category.get()
            database.del_category(category)
            self._make_settings_tab(self.nbTabs[1])
            self._make_general_tab(self.nbTabs[0])

    def _add_category(self, ev=None):
        """ Додати категорію
        """
        # Створення діалогового вікна
        tmp = Toplevel()
        tmp.title('New category')
        tmp.focus_set()
        tmp.grab_set()
        entry = ttk.Entry(tmp)
        entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(tmp, text="Ok", command=lambda ev=None: self._destroy_dialog(tmp, entry)).grid(row=1,
                                                                                                  column=2,
                                                                                                  padx=5,
                                                                                                  pady=5)
        tmp.wait_window()

        category = self._dialog_category     # атрибут, через який передається значення, введені користувачем
        self._dialog_category = ''           # затирається, щоб при повторному виклику не спрацював при порожніх полях
        if category:
            try:              # намагаємось додати і заповнити списки
                database.add_category(category)
                showinfo('Successful', 'Category is successfully added')
                self._make_general_tab(self.nbTabs[0])
                self._make_settings_tab(self.nbTabs[1])

            except Exception as e:
                showerror('Error', e)
                logging.exception(e)

    def _destroy_dialog(self, dialog, entry):
        """ Знищення діалогового вікна. Повинне зберегти введені значення

        :param dialog: діалогове вікно
        :param entry: поле для введення
        """
        self._dialog_category = entry.get()
        dialog.destroy()

    def _monitor(self, ev=None):
        """ Моніторить сайти і оновлює списки
        """
        self._nb_frame.destroy()
        # хотілось вивести діалогове вікно з повідомленням 'Monitoring', але не працює належним чином
        monitoring()
        self._make_widgets()

    def _save_database(self, ev=None):
        """ Зберегти результати моніторингу в ексель таблицю
        """
        path = asksaveasfilename(defaultextension='.xlsx')   # запит користувача назви файлу
        if path:
            data = database.get_items(item_type=LINK)
            translator = id_dict(database.get_categories())
            for el in data:
                el['Category'] = translator[el['Category_id']]
                del el['Category_id']
            try:
                create_xlsx(path, data)
                showinfo('Successful', 'All the links are successfully saved to {}'.format(path))
            except Exception as e:
                showerror('Error', e)
                logging.exception(e)


class DialogChangeSite:
    """ Діалогове вікно для зміни елемента
    """
    def __init__(self, default: dict, item_type=SITE):
        """ Конструктор

        :param default: значення елемента
        :param item_type: тип (SITE, KEY_WORD)
        """
        self.default = default
        self._type = item_type

        # в залежності від типу вибираємо відповідні списки полів
        self._fields = SITES_DATA_FIELDS if item_type == SITE else KEY_WORDS_DATA_FIELDS

        self.diag = Toplevel()
        self.diag.focus_set()
        self._widgets = {}
        self._make_widgets()

    def _make_widgets(self):
        """ Створити віджети
        """
        for i, el in enumerate(self._fields, 1):
            if el in ['Id', 'Category_id']:
                continue
            ttk.Label(self.diag, text=el + ':').grid(row=i, column=1, padx=5, pady=5)
            tmp = ttk.Entry(self.diag)
            tmp.grid(row=i, column=2, padx=5, pady=5, columnspan=2)
            self._widgets[el] = tmp
            tmp.insert(0, self.default[el])
        ttk.Button(self.diag, text='Change', command=self._confirm).grid(row=i+1, column=1, padx=5, pady=5)
        ttk.Button(self.diag, text='Delete', command=self._delete).grid(row=i+1, column=2, padx=5, pady=5)
        ttk.Button(self.diag, text='Cancel', command=self.diag.destroy).grid(row=i+1, column=3, padx=5, pady=5)

    def _confirm(self, ev=None):
        """ Підтвердити зміни і вийти.
        """
        if askyesno('Confirm', 'Save changes?'):
            params = {}
            for el in self._fields:
                if el in ['Id', 'Category_id']:
                    continue
                params[el] = self._widgets[el].get()
            try:
                database.change_item_id(self.default['Id'], item_type=self._type, **params)
                showinfo('Successful', 'Item is successfully updated.')
            except Exception as e:
                showerror('Error', e)
                logging.exception(e)
            self.diag.destroy()

    def _delete(self, ev=None):
        """ Видалити елемент і вийти.
        """
        if askyesno('Warning', 'Do you really want to delete this {}?'.format(self._type[:-1])):
            try:
                database.del_item(item_type=self._type, item_id=self.default['Id'])
                showinfo('Successful', 'Item is successfully updated.')
            except Exception as e:
                showerror('Error', e)
                logging.exception(e)
            self.diag.destroy()
