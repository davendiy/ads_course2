#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from .dialogs import *
import matplotlib.pyplot as plt
import numpy as np

# TODO add comments


class MainWindow(Tk):
    """ Головне вікно програми.

    Складається з 3-х вкладок: Головна, Усі доходи, Усі витрати

    'Головна' показує доходи за останній день/місяць + баланс за весь час
    'Усі доходи' і 'Усі витрати' дозволяють проглянути відповідно історію доходів і витрат
    за останній день/місяць/рік/весь_час + проводити пошук по категорії + додавання нової категорії,
    зміни існуючої транзакції (за допомогою подвійного натиснення на відповідний запис) та
    створення діаграми.
    """

    def __init__(self):
        Tk.__init__(self)
        self.database = BudgetDB(DEFAULT_DATABASE)
        self.data_connector = BudgetCollection(self.database)
        self._make_widgets()
        print(self.data_connector.balance)

    def _make_widgets(self):
        """ Створити віджети
        """
        self.title('Home budget')

        # Перераховуємо баланс (оскільки _make_widgets буде викликатись після кожної зміни бази даних)
        self.data_connector.update_balance()
        self._nb_frame = ttk.Frame(self)
        self._nb_frame.pack(side=TOP)
        self.nb = ttk.Notebook(self._nb_frame, width=620, height=300)  # створення вкладок
        self.nb.pack(padx=5)

        # додаємо 3 рамки, що стануть вкладками
        self.nbTabs = tuple([ttk.Frame(self._nb_frame) for _ in range(3)])
        self.nb.add(self.nbTabs[0], text='General', padding=2)
        self.nb.add(self.nbTabs[1], text='All the revenues', padding=2)
        self.nb.add(self.nbTabs[2], text='All the costs', padding=2)
        self._make_general_tab(self.nbTabs[0])
        self._make_revenues_tab(self.nbTabs[1])
        self._make_costs_tab(self.nbTabs[2])

    def _make_general_tab(self, main_frame):
        """ Заповнити Головну вкладку

        :param main_frame: рамка, до якої чіпляються віджети
        """
        # список-дерево доходів з кнопкою 'Додати'
        self._costs_tree = ttk.Treeview(main_frame, height=2, show='headings')
        self._costs_tree.grid(row=1, column=1, pady=10)
        self._costs_tree['columns'] = ('Costs', 'UAH')
        self._costs_tree.column("Costs", width=120, anchor='center')
        self._costs_tree.heading("Costs", text="Costs", anchor='center')
        self._costs_tree.column("UAH", width=120, anchor='center')
        self._costs_tree.heading("UAH", text="UAH", anchor='center')

        ttk.Button(main_frame, text='Add', command=self._add_cost_handler).grid(row=1, column=2, padx=5)

        # список-дерево витрат з кнопкою 'Додати'
        self._revenue_tree = ttk.Treeview(main_frame, height=1, show='headings')
        self._revenue_tree.grid(row=2, column=1, pady=10)
        self._revenue_tree['columns'] = ('Revenue', 'UAH')
        self._revenue_tree.column("Revenue", width=120, anchor='center')
        self._revenue_tree.heading("Revenue", text="Revenue", anchor='center')
        self._revenue_tree.column("UAH", width=120, anchor='center')
        self._revenue_tree.heading("UAH", text="UAH", anchor='center')

        ttk.Button(main_frame, text='Add', command=self._add_revenue_handler).grid(row=2, column=2, padx=5)

        # список-дерево балансу
        self._balance_tree = ttk.Treeview(main_frame, height=1, show='headings')
        self._balance_tree.grid(row=3, column=1, pady=10)
        self._balance_tree['columns'] = ('Balance', 'UAH')
        self._balance_tree.column("Balance", width=120, anchor='center')
        self._balance_tree.heading("Balance", text="Balance", anchor='center')
        self._balance_tree.column("UAH", width=120, anchor='center')
        self._balance_tree.heading("UAH", text="UAH", anchor='center')

        self._fill_trees()

    def _make_revenues_tab(self, main_frame):
        """ Заповнити віджетами вкладку 'Усі доходи'

        :param main_frame: рамка, до якої кріпляться віджети
        """
        # випадаюче меню вибору режиму відображення історії
        self._rev_chosen_type = StringVar(main_frame)
        option_menu = ttk.OptionMenu(main_frame, self._rev_chosen_type, 'All time', 'Day', 'Month', 'Year', 'All time')
        option_menu.config(width=10)
        option_menu.grid(row=1, column=1, padx=5, pady=5)

        # випадаюче меню вибору категорії
        self._rev_chosen_category = StringVar(main_frame)
        categories = self.data_connector.get_categories(item_type=REVENUE)
        tmp = name_dict(categories).keys()
        option_menu = ttk.OptionMenu(main_frame, self._rev_chosen_category, '', *tmp)
        option_menu.config(width=10)
        option_menu.grid(row=1, column=2, padx=5, pady=5)

        # рамка з списком-деревом і стрчкою прокрутки, що відображає результат пошуку
        _frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(_frame)
        self._all_rev_tree = ttk.Treeview(_frame, show='headings', yscrollcommand=scroll.set)
        self._all_rev_tree.bind('<Double-1>', lambda ev: self._change_item(item_type=REVENUE))
        scroll.config(command=self._all_rev_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self._all_rev_tree.pack(side=RIGHT)
        self._all_rev_tree['columns'] = REVENUE_FIELDS

        for el in REVENUE_FIELDS:
            self._all_rev_tree.column(el, width=120, anchor='center')
            self._all_rev_tree.heading(el, text=el, anchor='center')

        _frame.grid(row=2, column=1, columnspan=4)
        self._fill_revenue_tree()

        # кнопки
        ttk.Button(main_frame, text='Update', command=self._fill_revenue_tree).grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(main_frame, text='New category',
                   command=lambda **ev: self._add_category(REVENUE)).grid(row=3, column=2, padx=5, pady=5)

        ttk.Button(main_frame, text='Delete category',
                   command=lambda **ev: self._del_category(REVENUE)).grid(row=3, column=3, padx=5, pady=5)

        ttk.Button(main_frame, text='Histogram',
                   command=lambda **ev: self._make_hist(REVENUE)).grid(row=3, column=1, padx=5, pady=5)

    def _fill_revenue_tree(self, ev=None):
        """ Заповнити список-дерево результатів пошуку значеннями
        """
        # отримуємо елементи
        items = self.data_connector.get_items(item_type=REVENUE, category=self._rev_chosen_category.get())
        self._all_rev_tree.delete(*self._all_rev_tree.get_children())   # видаляємо попередні значення

        year, month, day = str(datetime.datetime.now().date()).split('-')

        # словник {"Category_name": "Category_id"}
        translator = id_dict(self.data_connector.get_categories(item_type=REVENUE))

        # виводимо елементи, які дозволені вибраним режимом (останній день/місяць...)
        for el in items:
            el['Category'] = translator[el['Category_id']]
            del el['Category_id']
            tmp_year, tmp_month, tmp_day = el['Date'].split('-')
            if self._rev_chosen_type.get() == 'Day' and any([tmp_year != year, tmp_month != month, tmp_day != day]):
                continue
            if self._rev_chosen_type.get() == 'Month' and (tmp_year != year or tmp_month != month):
                continue
            if self._rev_chosen_type.get() == 'Year' and (tmp_year != year):
                continue

            tmp = tuple(map(lambda a: el[a], REVENUE_FIELDS))
            self._all_rev_tree.insert('', 'end', text='', values=tmp)

    def _make_costs_tab(self, main_frame):
        """ Заповнити віджетами вкладку 'Усі витрати'

        :param main_frame: рамка, до якої кріпляться віджети
        """
        # все аналогічно _make_revenue_tab
        self._cost_chosen_type = StringVar(main_frame)
        option_menu = ttk.OptionMenu(main_frame, self._cost_chosen_type, 'All time', 'Day', 'Month', 'Year', 'All time')
        option_menu.config(width=10)
        option_menu.grid(row=1, column=1, padx=5, pady=5)

        self._cost_chosen_category = StringVar(main_frame)
        categories = self.data_connector.get_categories(item_type=COST)
        tmp = name_dict(categories).keys()
        print(tmp)
        option_menu = ttk.OptionMenu(main_frame, self._cost_chosen_category, '', *tmp)
        option_menu.config(width=10)
        option_menu.grid(row=1, column=2, padx=5, pady=5)

        _frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(_frame)
        self._all_cost_tree = ttk.Treeview(_frame, show='headings', yscrollcommand=scroll.set)
        self._all_cost_tree.bind('<Double-1>', lambda ev: self._change_item(item_type=COST))
        scroll.config(command=self._all_cost_tree.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self._all_cost_tree.pack(side=RIGHT)
        self._all_cost_tree['columns'] = COSTS_FIELDS

        for el in COSTS_FIELDS:
            self._all_cost_tree.column(el, width=120, anchor='center')
            self._all_cost_tree.heading(el, text=el, anchor='center')

        _frame.grid(row=2, column=1, columnspan=3)
        self._fill_costs_tree()

        ttk.Button(main_frame, text='Update', command=self._fill_costs_tree).grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(main_frame, text='New category',
                   command=lambda **ev: self._add_category(COST)).grid(row=3, column=2, padx=5, pady=5)

        ttk.Button(main_frame, text='Delete category',
                   command=lambda **ev: self._del_category(COST)).grid(row=3, column=3, padx=5, pady=5)

        ttk.Button(main_frame, text='Histogram',
                   command=lambda **ev: self._make_hist(COST)).grid(row=3, column=1, padx=5, pady=5)

    def _fill_costs_tree(self, ev=None):
        """ Заповнити список-дерево результатів пошуку значеннями
        """

        # все аналогічно _fill_revenues_tree
        items = self.data_connector.get_items(item_type=COST, category=self._cost_chosen_category.get())
        self._all_cost_tree.delete(*self._all_cost_tree.get_children())

        year, month, day = str(datetime.datetime.now().date()).split('-')
        translator = id_dict(self.data_connector.get_categories(item_type=COST))
        for el in items:
            el['Category'] = translator[el['Category_id']]
            del el['Category_id']
            tmp_year, tmp_month, tmp_day = el['Date'].split('-')
            if self._cost_chosen_type.get() == 'Day' and any([tmp_year != year, tmp_month != month, tmp_day != day]):
                continue
            if self._cost_chosen_type.get() == 'Month' and (tmp_year != year or tmp_month != month):
                continue
            if self._cost_chosen_type.get() == 'Year' and (tmp_year != year):
                continue

            tmp = tuple(map(lambda a: el[a], COSTS_FIELDS))
            self._all_cost_tree.insert('', 'end', text='', values=tmp)

    def _fill_trees(self):
        """ Заповнити значеннями дерева-списки з Головної вкладки
        """
        year, month, day = str(datetime.datetime.now().date()).split('-')
        self._costs_tree.delete(*self._costs_tree.get_children())
        self._revenue_tree.delete(*self._revenue_tree.get_children())
        self._balance_tree.delete(*self._balance_tree.get_children())

        tmp = self.data_connector.get_sum(year=year, month=month, item_type=COST, day=day)
        self._costs_tree.insert('', 'end', text='', values=('Day', tmp))

        tmp = self.data_connector.get_sum(year=year, month=month, item_type=COST)
        self._costs_tree.insert('', 'end', text='', values=('Month', tmp))

        tmp = self.data_connector.get_sum(year=year, month=month, item_type=REVENUE)
        self._revenue_tree.insert('', 'end', text='', values=('Month', tmp))

        self._balance_tree.insert('', 'end', text='', values=('All time', self.data_connector.balance))

    def _add_cost_handler(self, ev=None):
        """ Обробити натиснення кнопки 'Додати' на Головній вкладці навпроти витрат.
        """
        tmp = DialogAddItem(self, COST)
        self.wait_window(tmp.diag)
        self._nb_frame.destroy()
        self._make_widgets()

    def _add_revenue_handler(self, ev=None):
        """ Обробити натиснення кнопки 'Додати' на Головній вкладці навпроти доходів
        """
        tmp = DialogAddItem(self, REVENUE)
        self.wait_window(tmp.diag)
        self._nb_frame.destroy()
        self._make_widgets()

    def _change_item(self, item_type):
        """ Обробити подвійне натиснення на лемент списку
         з вкладки 'Усі доходи' або 'Усі витрати'.

        :param item_type: REVENUE or COST
        """
        # формуємо відповідні значення за умовчанням для витрат або доходів (залежно від item_type)
        if item_type == REVENUE:
            item = self._all_rev_tree.focus()
            _default = dict(zip(REVENUE_FIELDS, self._all_rev_tree.item(item)['values']))
        else:
            item = self._all_cost_tree.focus()
            _default = dict(zip(COSTS_FIELDS, self._all_cost_tree.item(item)['values']))

        tmp = DialogChangeItem(self, item_type, _default)
        self.wait_window(tmp.diag)
        self._nb_frame.destroy()
        self._make_widgets()
        if item_type == REVENUE:           # вибираємо вкладку, з якої викликалась команда
            tab = self.nbTabs[1]
        else:
            tab = self.nbTabs[2]
        self.nb.select(tab)

    def _add_category(self, item_type):
        """

        :param item_type:
        :return:
        """
        tmp = DialogAddCategory(self, item_type)
        self.wait_window(tmp.diag)
        self._nb_frame.destroy()
        self._make_widgets()
        if item_type == REVENUE:
            tab = self.nbTabs[1]
        else:
            tab = self.nbTabs[2]
        self.nb.select(tab)

    def _del_category(self, item_type):
        tmp = DialogDelCategory(self, item_type)
        self.wait_window(tmp.diag)
        self._nb_frame.destroy()
        self._make_widgets()
        if item_type == REVENUE:
            tab = self.nbTabs[1]
        else:
            tab = self.nbTabs[2]
        self.nb.select(tab)

    def _make_hist(self, item_type):
        categories = name_dict(self.data_connector.get_categories(item_type))
        counter = {}
        for k, v in categories.items():
            counter[k] = self.data_connector.get_sum(item_type=item_type, Category_id=v)

        labels, values = zip(*counter.items())

        indexes = np.arange(len(labels))
        width = 0.8

        plt.bar(indexes, values, width)
        plt.xticks(indexes + width * 0.5, labels)
        plt.show()
