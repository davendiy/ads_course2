#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter.messagebox import showwarning, showinfo
from dz_others.subject24_gui.t24_22.ms_module import *


PATTERN = "ID: {}, DEPART: {}, ARRIVE: {}, CLASS: {}, COST: {}"   # шаблон виведення


class Dialog:
    """ Клас, який реалізує діалогове вікно,
        в якому необхідно вибрати рейс
    """

    def __init__(self, res_list):
        """ Ініціалізація

        :param res_list: список кортежів з ms_module
        """
        self.diag = Toplevel()     # створюємо діалогове вікно
        self.diag.focus_set()      # переключаємо фокус на нього
        self.diag.grab_set()
        self._data = res_list
        self._make_widgets()

    def _make_widgets(self):
        """ Створення віджетів
        """
        # рамка з Listbox - список доступних рейсів
        Label(self.diag, text=' Результати пошуку:', font=('Helvetica', '12', 'bold')).pack(side=TOP)
        self.frame = Frame(self.diag)
        self.scroll = Scrollbar(self.frame)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.airports = Listbox(self.frame, height=15,
                                width=50, yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.airports.yview)
        self.airports.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.frame.pack(side=LEFT, fill=BOTH, expand=YES)
        self.airports.bind('<Double-1>', self._handler)

        for flight in self._data:                                     # type: Flight
            self.airports.insert(END, PATTERN.format(*flight))

        # Кнопка ок
        Button(self.diag, command=self._handler, text='Ok').pack(side=BOTTOM)
        self.diag.update()

    def _handler(self, ev=None):
        """ Дія, яка викликається подвійним натисненням на елемент
            списку, або натисненням на кнопку ок

        :param ev:
        :return:
        """
        showinfo(message='Choice was being done successfully')
        self.diag.destroy()


class GUI:
    """ Графічний інтерфейс.
        Головне вікно містить 2 списки - доступні аеропорти.
        Вибір аеропорту реалізується подвійним натисненням.
        Для того, щоб знайти необхідний рейс, треба вибрати аеропорти, записати
        необхідну дату у вказаному форматі і натиснути на кнопку find.
    """

    def __init__(self, master):
        """ Ініціалізація

        :param master: вікно, до якого прив'язаний графічний інтерфейс
        """
        self.top = master
        self.filename = 'data.xlsx'     # ексель таблиця
        self.sheet_flights = 'Flights'      # необхідні аркуші
        self.sheet_airports = 'Airports'

        self._map = None        # словник {назва аеропорту: ід}
        self._update_airports()
        self._make_widgets()
        self._from = None
        self._to = None

    def _update_airports(self):
        """ Загружає список аеропортів з ексель таблиці.
        """
        self._map = get_all_airports(self.filename, self.sheet_airports)

    def _make_widgets(self):
        """ Створення віджетів
        """
        # написи вгорі вікна
        self.frame_labels = Frame(self.top)
        Label(self.frame_labels, text='    FROM', font=('Helvetica', '12', 'bold')).pack(side=LEFT)
        Label(self.frame_labels, text='TO    ', font=('Helvetica', '12', 'bold')).pack(side=RIGHT)
        self.frame_labels.pack(side=TOP, fill=X)

        self._make_lists()    # списки аеропортів

        # вибрані аеропорти
        self.frame_chosen = Frame(self.top)
        Label(self.frame_chosen, text='From', font=('arial', '16', 'bold')).pack(side=LEFT)
        self.output1 = Label(self.frame_chosen, font=('arial', '16'))
        self.output1.pack(side=LEFT)
        Label(self.frame_chosen, text='TO', font=('arial', '16', 'bold')).pack(side=LEFT)
        self.output2 = Label(self.frame_chosen, font=('arial', '16'))
        self.output2.pack(side=LEFT)

        self.frame_chosen.pack(side=TOP, fill=X)

        # рядок введення дати
        Label(self.top, text='Дата у форматі dd.mm.yyyy:', font=('arial', '16')).pack(side=LEFT)
        self.input = Entry(self.top, font=('arial', '16'))
        self.input.pack(side=LEFT)

        # кнопка запуску
        Button(self.top, text='Find!', font=('Helvetica', '16'), command=self._find_handler).pack(side=RIGHT)

    def _make_lists(self):
        """ Створення 2-х списків у рамці
        """
        self._lists = Frame(self.top)
        self._from_air_frame = Frame(self._lists)
        self._from_scroll = Scrollbar(self._from_air_frame)
        self._from_scroll.pack(side=RIGHT, fill=Y)
        self._from_list = Listbox(self._from_air_frame, height=15,
                                  width=50, yscrollcommand=self._from_scroll.set)
        self._from_scroll.config(command=self._from_list.yview)
        self._from_list.pack(side=RIGHT, fill=BOTH, expand=YES)
        self._from_air_frame.pack(side=LEFT, fill=Y, expand=YES)

        self._from_list.bind('<Double-1>', self._left_handler)

        self._fill_list(self._from_list, self._map)

        self._to_air_frame = Frame(self._lists)
        self._to_scroll = Scrollbar(self._to_air_frame)
        self._to_scroll.pack(side=RIGHT, fill=Y)
        self._to_list = Listbox(self._to_air_frame, height=15,
                                width=50, yscrollcommand=self._to_scroll.set)
        self._to_scroll.config(command=self._to_list.yview)
        self._to_list.pack(side=RIGHT, fill=BOTH, expand=YES)
        self._to_air_frame.pack(side=LEFT, fill=Y, expand=YES)

        self._to_list.bind('<Double-1>', self._right_handler)

        self._fill_list(self._to_list, self._map)
        self._lists.pack(side=TOP, fill=X, expand=YES)

    def _fill_list(self, listbox: Listbox, map_dict: dict):
        """ Наповнення списків інформацією
        """
        for airport in map_dict:
            listbox.insert(END, airport)
        self.top.update()

    def _left_handler(self, ev=None):
        """Обробити подвійне натиснення лівої клавіші миші для лівого списку"""
        try:
            # отримати вибраний елемент списку
            check = self._from_list.get(self._from_list.curselection())
            self.output1.config(text=check)
            self._from = check

        except TclError:
            # пропустити помилку curselection, якщо під час
            # подвійного натиснення лівої клавіші миші список порожній
            pass
        except Exception as e:
            # якщо інша помилка, то видати повідомлення
            showwarning('Помилка', e)
            raise e                   # і виключення для логування у файл

    def _right_handler(self, ev=None):
        """Обробити подвійне натиснення лівої клавіші миші."""
        try:
            # отримати вибраний елемент списку
            check = self._to_list.get(self._to_list.curselection())
            self.output2.config(text=check)
            self._to = check
        except TclError:
            # пропустити помилку curselection, якщо під час
            # подвійного натиснення лівої клавіші миші список порожній
            pass
        except Exception as e:
            # якщо інша помилка, то видати повідомлення
            showwarning('Помилка', e)
            raise e                     # і виключення для логування у файл

    def _find_handler(self):

        """Обробити подвійне натиснення лівої клавіші миші."""
        try:
            # отримати вибраний елемент списку
            date = self.input.get()
            if not date or self._from is None or self._to is None:
                return

            date = tuple(map(int, reversed(date.split('.'))))
            air_id1 = self._map[self._from]
            air_id2 = self._map[self._to]

            res = get_all_flights(self.filename, air_id1, air_id2, date, self.sheet_flights)

            Dialog(res)

        except TclError:
            # пропустити помилку curselection, якщо під час
            # подвійного натиснення лівої клавіші миші список порожній
            pass
        except Exception as e:
            # якщо інша помилка, то видати повідомлення
            showwarning('Помилка', e)
            raise e                         # і виключення для логування у файл


if __name__ == '__main__':
    import sys

    # перевизначаємо стандартний потік виключень, щоб помилки виводились у файл
    sys.stderr = open('gui.log', 'a', encoding='utf-8')
    sys.stderr.write('\n\n-----------{}----------\n'.format(datetime.datetime.now()))

    top = Tk()
    test = GUI(top)
    mainloop()

    sys.stderr.close()   # перед виходом з програми обов'язково закрити файл
