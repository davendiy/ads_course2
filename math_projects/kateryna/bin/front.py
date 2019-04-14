#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import datetime
from .dialogs import *

from tkinter.messagebox import showwarning
from webbrowser import open

from urllib.request import urlopen
from urllib.request import HTTPError

now_date = datetime.datetime.now().date()


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self._dialog_category = ''
        self._make_widgets()

    def _make_widgets(self):
        self.title('MonitorGui')
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

        # --------------------------Buttons---------------------------------------

        ttk.Label(main_frame, text='From:').grid(row=1, column=1, padx=5, pady=5)
        self._date_from = ttk.Entry(main_frame, width=12)
        self._date_from.insert(0, '2000-01-01')
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
        tmp = self._gen_chosen_category.get()
        if self._date_from.get():
            try:
                date_from = list(map(int, self._date_from.get().split('-')))
                date_to = list(map(int, self._date_to.get().split('-')))
                date_from = datetime.datetime(*date_from)
                date_to = datetime.datetime(*date_to)
            except Exception as e:
                showerror('Error', 'Please, enter the correct date.')
                logging.exception(e)
                return
        else:
            date_from = datetime.datetime.min
            date_to = datetime.datetime.max

        tmp = database.get_category_id(tmp)
        items = database.get_items(item_type=LINK, category=tmp)
        self._monitor_tree.delete(*self._monitor_tree.get_children())  # видаляємо попередні значення

        # словник {"Category_name": "Category_id"}
        translator = id_dict(database.get_categories())

        # виводимо елементи, які дозволені вибраним режимом (останній день/місяць...)
        for el in items:
            el['Category'] = translator[el['Category_id']]
            del el['Category_id']

            el['Date'] = el['Date'][:el['Date'].rindex('.')]
            tmp_date = datetime.datetime(*map(int, el['Date'].split()[0].split('-')))
            if not date_from <= tmp_date <= date_to:
                continue
            tmp = tuple(map(lambda a: el[a], LINKS_GUI_FIELDS))
            self._monitor_tree.insert('', 0, text='', values=tmp)

    def _make_settings_tab(self, main_frame):
        self._set_chosen_category = StringVar(main_frame)
        categories = id_dict(database.get_categories())
        chosen_cat = '' if not categories else next(iter(categories.values()))
        option_menu = ttk.OptionMenu(main_frame, self._set_chosen_category, chosen_cat, *categories.values())
        option_menu.config(width=20)
        option_menu.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(main_frame, text="Update", command=self._fill_settings).grid(row=1, column=3, padx=5, pady=5)

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

        self._site_name = ttk.Entry(main_frame)
        self._site_name.grid(row=3, column=1, padx=5, pady=5)
        self._site_name.insert(0, 'Name')
        self._site_url = ttk.Entry(main_frame)
        self._site_url.grid(row=3, column=2, padx=5, pady=5)
        self._site_url.insert(0, 'http://www.link.com')

        self._word = ttk.Entry(main_frame)
        self._word.grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text='Add', command=self._add_site).grid(row=3, column=3, padx=5, pady=5)
        ttk.Button(main_frame, text='Add', command=self._add_word).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(main_frame, text='Delete category', command=self._delete_category).grid(row=1,
                                                                                           column=2,
                                                                                           padx=5,
                                                                                           pady=5)
        ttk.Button(main_frame, text='New category', command=self._add_category).grid(row=5, column=3, padx=5, pady=5)

    def _run_browser(self, ev=None):
        item = self._monitor_tree.focus()
        params = dict(zip(LINKS_GUI_FIELDS, self._monitor_tree.item(item)['values']))
        open(params['Link'])

    def _change_site(self, ev=None):
        item = self._sites_tree.focus()
        _default = dict(zip(SITES_GUI_FIELDS, self._sites_tree.item(item)['values']))
        tmp = DialogChangeSite(self, _default, item_type=SITE)
        tmp.diag.wait_window()
        self._fill_settings()

    def _change_word(self, ev=None):
        item = self._words_tree.focus()
        _default = dict(zip(KEY_WORDS_GUI_FIELDS, self._words_tree.item(item)['values']))
        tmp = DialogChangeSite(self, _default, item_type=KEY_WORD)
        tmp.diag.wait_window()
        self._fill_settings()

    def _fill_settings(self, ev=None):
        category = self._set_chosen_category.get()
        category = database.get_category_id(category)

        self._sites_tree.delete(*self._sites_tree.get_children())  # видаляємо попередні значення
        self._words_tree.delete(*self._words_tree.get_children())  # видаляємо попередні значення

        items = database.get_items(item_type=SITE, category=category)
        for el in items:
            del el['Category_id']
            tmp = tuple(map(lambda a: el[a], SITES_GUI_FIELDS))
            self._sites_tree.insert('', 0, text='', values=tmp)

        items = database.get_items(item_type=KEY_WORD, category=category)
        for el in items:
            del el['Category_id']
            tmp = tuple(map(lambda a: el[a], KEY_WORDS_GUI_FIELDS))
            self._words_tree.insert('', 0, text='', values=tmp)

    def _add_word(self, ev=None):
        word = self._word.get()
        if word:
            category = self._set_chosen_category.get()
            category = database.get_category_id(category)
            database.add_item(item_type=KEY_WORD, Word=word, Category_id=category)
            self._fill_settings()

    def _add_site(self, ev=None):
        name = self._site_name.get()
        link = self._site_url.get()

        try:
            urlopen(link)
        except HTTPError:
            showwarning('Warning', "Couldn't open {}".format(link))
        except Exception as e:
            showerror('Error', 'Please, enter the correct url')
            logging.exception(e)
            return

        if name and link:
            category = self._set_chosen_category.get()
            category = database.get_category_id(category)
            database.add_item(item_type=SITE, Name=name, Link=link, Category_id=category)
            self._fill_settings()

    def _delete_category(self, ev=None):
        if askyesno('Warning', 'Do you really want to delete this category (all the results of '
                               'monitoring for this category will be deleted)?'):
            category = self._set_chosen_category.get()
            database.del_category(category)
            self._make_settings_tab(self.nbTabs[1])
            self._make_general_tab(self.nbTabs[0])

    def _add_category(self, ev=None):
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

        category = self._dialog_category
        self._dialog_category = ''

        if category:
            try:
                database.add_category(category)
                showinfo('Successful', 'Category is successfully added')
                self._make_general_tab(self.nbTabs[0])
                self._make_settings_tab(self.nbTabs[1])

            except Exception as e:
                showerror('Error', e)
                logging.exception(e)

    def _destroy_dialog(self, dialog, entry):
        self._dialog_category = entry.get()
        dialog.destroy()
