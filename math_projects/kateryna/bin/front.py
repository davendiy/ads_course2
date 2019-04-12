#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from .dialogs import *
from tkinter import *
from tkinter import ttk
import datetime
from .database import *
from webbrowser import open

now_date = datetime.datetime.now().date()


class MainWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self._make_widgets()

    def _make_widgets(self):
        self.title('MonitorGui')
        self._nb_frame = ttk.Frame(self)
        self._nb_frame.pack(side=TOP)
        self.nb = ttk.Notebook(self._nb_frame, height=300)
        self.nb.pack(padx=5)

        self.nbTabs = tuple([ttk.Frame(self._nb_frame) for _ in range(2)])
        self.nb.add(self.nbTabs[0], text='Monitoring', padding=2)
        self.nb.add(self.nbTabs[1], text='Settings', padding=2)
        self._make_general_tab(self.nbTabs[0])
        self._make_settings_tab(self.nbTabs[1])

    def _make_general_tab(self, main_frame):

        # --------------------------Buttons---------------------------------------
        self._date_from = '2000-01-01'
        self._date_to = str(now_date)

        self._button_from = ttk.Button(main_frame, text='From ' + self._date_from, command=self._from_handler)
        self._button_from.grid(row=1, column=1, padx=5, pady=5)

        self._button_to = ttk.Button(main_frame, text='To ' + self._date_to, command=self._from_handler)
        self._button_to.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(main_frame, text='Update', command=self._fill_monitor_tree).grid(row=1, column=4, padx=5, pady=5)
        # -------------------------OptionMenu------------------------------------
        self._gen_chosen_category = StringVar(main_frame)
        categories = id_dict(database.get_categories())
        option_menu = ttk.OptionMenu(main_frame, self._gen_chosen_category, '...', *categories.values(), '...')
        option_menu.config(width=10)
        option_menu.grid(row=1, column=3, padx=5, pady=5)

        # --------------------------TreeView--------------------------------------
        _frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(_frame)
        self._monitor_tree = ttk.Treeview(_frame, show='headings', yscrollcommand=scroll.set)
        scroll.config(command=self._monitor_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self._monitor_tree['columns'] = LINKS_FIELDS
        self._monitor_tree.pack(side=RIGHT)
        for el in LINKS_FIELDS:
            self._monitor_tree.column(el, width=180, anchor='center')
            self._monitor_tree.heading(el, text=el, anchor='center')

        self._monitor_tree.bind('<Double-1>', self._run_browser)
        _frame.grid(row=2, column=1, columnspan=4)
        self._fill_monitor_tree()

    def _fill_monitor_tree(self, ev=None):
        tmp = self._gen_chosen_category.get()
        translator = name_dict(database.get_categories())
        tmp = translator.get(tmp, '')

        items = database.get_items(item_type=LINK, category=tmp)
        self._monitor_tree.delete(*self._monitor_tree.get_children())   # видаляємо попередні значення

        # словник {"Category_name": "Category_id"}
        translator = id_dict(database.get_categories())

        # виводимо елементи, які дозволені вибраним режимом (останній день/місяць...)
        for el in items:
            el['Category'] = translator[el['Category_id']]
            del el['Category_id']

            el['Date'] = el['Date'][:el['Date'].rindex('.')]
            tmp = tuple(map(lambda a: el[a], LINKS_FIELDS))
            self._monitor_tree.insert('', 'end', text='', values=tmp)
        ...

    def _make_settings_tab(self, main_frame):
        ...

    def _from_handler(self, ev=None):
        ...

    def _run_browser(self, ev=None):
        item = self._monitor_tree.focus()
        params = dict(zip(LINKS_FIELDS, self._monitor_tree.item(item)['values']))
        open(params['Link'])
