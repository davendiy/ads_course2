#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter.messagebox import showwarning


class Dialog:
    """ Діалогове вікно для вказання параметрів пошуку
    """

    def __init__(self, prev):
        """ Ініціалізація
        :param prev: вікно, яке викликало
        """
        self.prev = prev
        self.top = Toplevel()
        self.top.focus_set()
        self.top.grab_set()
        self._make_widgets()

    def _make_widgets(self):
        """ Створення віджетів
        """
        _frame_entry1 = Frame(self.top)
        _frame_entry2 = Frame(self.top)    # рамки для написів і полів для введення
        _frame_entry3 = Frame(self.top)

        # написи (кожен у своїй рамці)
        Label(_frame_entry1, text='Name: ', font=('arial', '16', 'bold')).pack(side=LEFT)
        Label(_frame_entry2, text='Author: ', font=('arial', '16', 'bold')).pack(side=LEFT)
        Label(_frame_entry3, text='Year of publication: ', font=('arial', '16', 'bold')).pack(side=LEFT)

        # поля для введення (кожне у своїй рамці
        self._name = Entry(_frame_entry1, font=('arial', '16'))
        self._name.pack(side=RIGHT, fill=X)
        self._author = Entry(_frame_entry2, font=('arial', '16'))
        self._author.pack(side=RIGHT, fill=X)
        self._year = Entry(_frame_entry3, font=('arial', '16'))
        self._year.pack(side=RIGHT, fill=X)

        # пакування рамок
        _frame_entry1.pack(side=TOP, fill=X)
        _frame_entry2.pack(side=TOP, fill=X)
        _frame_entry3.pack(side=TOP, fill=X)

        Button(self.top, text='Ok', command=self._ok_handler).pack(side=RIGHT)

    def _ok_handler(self, ev=None):
        """ Обробка натиснення кнопки
        """
        name = self._name.get()       # зчитуємо введені дані
        author = self._author.get()
        year = self._year.get()
        if not any([name, author, year]):   # хоча б одне поле має бути заповненим
            return

        # викликаємо функцію заповнення списку для класу, що викликав
        self.prev.fill(name.lower(), author.lower(), year.lower())
        self.top.destroy()


class GUI:
    """ Графічний інтерфейс.
    Головне вікно містить список, в якому відображається
    результат пошуку.
    """

    _pattern = "Name: {}, author: {}, year of publication: {}"    # шаблон виведення результату

    def __init__(self, master):
        """ Ініціалізація

        :param master: вікно, до якого прив'язаний графічний інтерфейс
        """
        self.top = master
        self.filename = 'data.in'     # файл, у якому містить інформація
        self.params = ('', '', '')
        self._data = []
        self._update_base()          # завантажити список
        self._make_widgets()         # зробити віджети

    def _update_base(self):
        """ Завантаження інформації з файлу
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            self._data.clear()
            for line in file:
                if not line.strip():
                    continue
                name, author, year = line.split()
                self._data.append((name, author, year))

    def _make_widgets(self):
        """ Створення віджетів
        """
        # напис у верхній частині вікна
        Label(self.top, text='    RESULT', font=('Helvetica', '12', 'bold')).pack(side=TOP)

        # рамка зі списком
        _list_frame = Frame(self.top)
        _scroll = Scrollbar(_list_frame)
        _scroll.pack(side=RIGHT, fill=Y)
        self._list = Listbox(_list_frame, height=15, width=50, yscrollcommand=_scroll)
        _scroll.config(command=self._list.yview)
        self._list.pack(side=RIGHT, fill=BOTH, expand=YES)
        _list_frame.pack()

        # рамка з написом і полем для введення
        _input_frame = Frame(self.top)
        Label(_input_frame, text='Limit of results: ', font=('arial', '16', 'bold')).pack(side=LEFT)
        self._limit = Entry(_input_frame, font=('arial', '16'))
        self._limit.pack(side=RIGHT, fill=X)
        _input_frame.pack(fill=X)

        # кнопка пошуку
        Button(self.top, text='find!',
               font=('arial', '16', 'bold'), command=self._find_handler).pack(side=RIGHT, padx=40)

    def _find_handler(self, ev=None):
        """ Обробляє натиснення кнопки.
        Викликає діалогове вікно для введення параметрів пошуку
        """
        Dialog(self)

    def fill(self, *params):
        """ Наповнення списку інформацією про книги з
        заданими параметрами

        :param params: author, name, year - рядки
        """
        try:
            limit = self._limit.get()      # якщо поле з обмеженням пусте, то вважаємо,
            limit = int(limit) if limit else float('inf')   # що обмеження == нескінченність
            length = 0
            self._list.delete(0, END)      # видаляємо зі списку всю інформацію

            for el in self._data:          # проходимо по всіх елементах бази
                if params[0] and el[0].lower() != params[0]:   # перевіряємо рівність кожного параметра
                    continue                                   # якщо він не пустий
                if params[1] and el[1].lower() != params[1]:
                    continue
                if params[2] and el[2].lower() != params[2]:
                    continue

                self._list.insert(END, GUI._pattern.format(*el))  # вставляємо у список ті, які пройшли перевірку
                length += 1
                if length == limit:    # якщо перевищили ліміт - зупинка
                    return
        except Exception as e:
            showwarning('Eror', e)             # якщо виникла якась помилка - виводимо на екран


if __name__ == '__main__':
    test_top = Tk()
    test = GUI(test_top)
    test_top.mainloop()
