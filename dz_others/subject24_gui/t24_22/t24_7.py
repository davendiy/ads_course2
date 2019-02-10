#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 28.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from tkinter import *


class Dialog:
    """ Діалогове вікно, в якому необхідно ввести n
        координат вектора.
    """
    def __init__(self, n: int, a: float, b: float, reason_window):
        """ Ініціалізація

        :param n: к-ть компонент вектора
        :param a: ліва межа відрізку
        :param b: права межа відрізку
        :param reason_window: вікно, яке спричинило даний екземпляр класу
        """
        self._top = Toplevel()
        self._top.focus_set()
        self._top.grab_set()
        self._reason = reason_window
        self._a = a
        self._b = b
        self._make_widgets(n)

    def _make_widgets(self, n):
        """ Створення віджетів

        :param n: к-ть компонент вектора (полів для введення)
        """
        self._all_input = []                # список полів введення
        for i in range(n):
            # для кожного поля введення буде пояснювальне текстове поле
            # обидва поля знаходяться в рамці
            tmp_frame = Frame(self._top)
            Label(tmp_frame, text='x{}:'.format(i), font=('arial', '16', 'bold')).pack(side=LEFT)
            tmp_input = Entry(tmp_frame, font=('arial', '16'))
            tmp_input.pack(side=LEFT)
            self._all_input.append(tmp_input)
            tmp_frame.pack(side=TOP)

        Button(self._top, text='Ok', command=self._ok_handler).pack(side=RIGHT)

    def _ok_handler(self):
        """ Функція, яку викликає кнопка ок
        """
        res = []
        for _input in self._all_input:   # зчитуємо всі поля для введення
            res.append(_input.get())

        if not all(res):                 # якщо хоч одне порожнє - припиняємо роботу функції
            return

        # інакше - оновлюємо список вікна, яке викликало self
        self._reason.update_list(res, self._a, self._b)
        self._top.destroy()               # знищуємо діалогове вікно


class MainWindow:
    """ Клас, який реалізує головне вікно
    """

    # шаблон виведення результату
    _pattern = 'Number of components, that are in section [a, b]:      {}'

    def __init__(self, master):
        self.top = master
        self._make_widgets()

    def _make_widgets(self):
        """ Створення віджетів
        """
        _frame1 = Frame(self.top)
        Label(_frame1, text='n:', font=("arial", '16', 'bold')).pack(side=LEFT)
        self._n = Entry(_frame1, font=('arial', '16'))
        self._n.pack(side=LEFT)
        _frame1.pack(side=TOP)

        _frame2 = Frame(self.top)
        Label(_frame2, text='a:', font=("arial", '16', 'bold')).pack(side=LEFT)
        self._a = Entry(_frame2, font=('arial', '16'))
        self._a.pack(side=LEFT)
        _frame2.pack(side=TOP)

        _frame3 = Frame(self.top)
        Label(_frame3, text='b:', font=("arial", '16', 'bold')).pack(side=LEFT)
        self._b = Entry(_frame3, font=('arial', '16'))
        self._b.pack(side=LEFT)
        _frame3.pack(side=TOP)

        _frame4 = Frame(self.top)
        Button(_frame4, text='Calculate', font=('arial', '16', 'bold'), command=self._handler).pack(side=RIGHT)
        _frame4.pack(side=TOP, fill=X)

        _frame5 = Frame(self.top)
        self._scroll = Scrollbar(_frame5)
        self._list = Listbox(_frame5, height=15, width=50, yscrollcommand=self._scroll.set)
        self._scroll.config(command=self._list.yview)
        self._scroll.pack(side=RIGHT, fill=Y)
        self._list.pack(side=RIGHT, fill=BOTH, expand=YES)
        _frame5.pack(side=TOP, fill=BOTH, expand=YES)

        self._answer = Label(self.top, text=MainWindow._pattern.format(''), font=('arial', '16', 'bold'))
        self._answer.pack(side=RIGHT)

    def _handler(self):
        """ Функція, яку викликає кнопка 'calculate'
        """
        a = self._a.get()
        b = self._b.get()       # зчитуємо поля введення
        n = self._n.get()

        if not all([a, b, n]):  # якщо хоч одне пусте - припиняємо роботу функції
            return

        Dialog(int(n), float(a), float(b), self)   # викликаємо діалогове вікно

    def update_list(self, vector, a, b):
        """ Оновлення списку компонент вектора

        :param vector: список дійсних чисел
        :param a: ліва межа відрізку
        :param b: права межа відрізку
        """
        self._list.delete(0, END)
        count = 0
        for el in vector:         # проходимо по всіх компонентах вектора
            if float(a) <= float(el) <= float(b):   # перевіряємо належність відрізку
                count += 1
            self._list.insert(END, el)              # вставляємо у список
        self._list.update()
        self._answer.config(text=MainWindow._pattern.format(count))   # виводимо результат


if __name__ == '__main__':
    top = Tk()
    test = MainWindow(top)
    top.mainloop()
