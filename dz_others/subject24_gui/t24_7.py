#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter.messagebox import showwarning


class Dialog:
    """ Діалогове вікно.
    Містить n полів для введення компонент вектора.
    """

    def __init__(self, n, pre):
        """ Ініціалізація

        :param n: к-ть компонент
        :param pre: вікно, яке визвало
        """
        self.pre = pre
        self._n = n
        self.top = Toplevel()
        self.top.focus_set()
        self.top.grab_set()
        self._make_widgets()

    def _make_widgets(self):
        """ Сворення віджетів
        """
        self._entries = []          # список всіх полів для введення
        for i in range(self._n):    # створення n рамок з написом і полем для введення
            _frame = Frame(self.top)
            _frame.pack(side=TOP, fill=X)   # рамка

            # напис
            Label(_frame, text='a[{}]: '.format(i), font=('arial', '16', 'bold')).pack(side=LEFT)

            # поле для введення
            tmp_entry = Entry(_frame, font=('arial', '16'))
            tmp_entry.pack(side=RIGHT, fill=X)
            self._entries.append(tmp_entry)

        # кнопка завершення
        Button(self.top, text='Ok', font=('arial', '16', 'bold'),
               command=self._ok_handler).pack(side=RIGHT)

    def _ok_handler(self, ev=None):
        """ Обробка натиснення кнопки
        """
        res = []
        for entry in self._entries:  # зчитуємо всі координати
            tmp = entry.get()
            if not tmp:              # якщо хоч одне поле пусте - відмова
                return

            res.append(float(tmp))
        self.pre.check(res)          # запускаємо функцію у вікні, яке викликало
        self.top.destroy()


class GUI:
    """ Головне вікно
    Містить список компонент вектора (спочатку пустий),
    поля для введення a, b, n (а також написи, які їх описують),
    напис з результатом і кнопку
    """

    _pattern = "Result: {}"   # шаблон виведення

    def __init__(self, master):
        self.top = master
        self._make_widgets()

    def _make_widgets(self):
        """ Створення віджетів
        """
        # заголовок
        Label(self.top, text='VECTOR', font=('Helvetica', '12', 'bold')).pack(side=TOP, fill=X)

        _frame1 = Frame(self.top)
        _frame2 = Frame(self.top)     # рамки
        _frame3 = Frame(self.top)
        _frame4 = Frame(self.top)

        _scroll = Scrollbar(_frame1)
        _scroll.pack(side=RIGHT, fill=Y)    # в першій рамці список з прокруткою
        self._list = Listbox(_frame1, height=15, width=50, yscrollcommand=_scroll)
        _scroll.config(command=self._list.yview)
        self._list.pack(side=RIGHT, fill=BOTH, expand=YES)

        self._a = Entry(_frame2, font=('arial', '16'))
        self._b = Entry(_frame3, font=('arial', '16'))  # поля для введення
        self._n = Entry(_frame4, font=('arial', '16'))
        self._a.pack(side=RIGHT, fill=X)
        self._b.pack(side=RIGHT, fill=X)
        self._n.pack(side=RIGHT, fill=X)

        # написи
        Label(_frame2, text="a: ", font=('arial', '16', 'bold')).pack(side=RIGHT)
        Label(_frame3, text="b: ", font=('arial', '16', 'bold')).pack(side=RIGHT)
        Label(_frame4, text="n: ", font=('arial', '16', 'bold')).pack(side=RIGHT)

        _frame1.pack(side=TOP, fill=X)
        _frame2.pack(side=TOP, fill=X)
        _frame3.pack(side=TOP, fill=X)
        _frame4.pack(side=TOP, fill=X)

        # напис з результатом
        self._res = Label(self.top, text=self._pattern.format(''), font=('arial', '16', 'bold'))
        self._res.pack(side=TOP, fill=X)
        Button(self.top, text='input', font=('arial', '16', 'bold'),
               command=self._input_handler).pack(side=RIGHT)

    def _input_handler(self, ev=None):
        """ Обробляє натиснення кнопки
        """
        try:
            a = self._a.get()    # зчитуємо поля для введення
            b = self._b.get()
            n = self._n.get()
            if not all([a, b, n]):   # якщо хоч одне пцсте - відмова
                return

            float(b)
            float(a)    # спроба перевести межі в числа (якщо помилка - виведення)
            Dialog(int(n), self)
        except Exception as e:
            showwarning('Error', e)

    def check(self, vector: list):
        """ Заповнення списку компонентами вектора і обчислення скільки
        компонент належать відрізку

        :param vector: список дійсних чисел
        """
        a = float(self._a.get())    # межі
        b = float(self._b.get())
        count = 0                   # к-ть компонент, які належать
        self._list.delete(0, END)
        for i, el in enumerate(vector):   # проходимо по всіх компонентах
            if a <= el <= b:              # перевіряємо, чи належить відрізку
                count += 1
            self._list.insert(END, f'a[{i}]: {el}')   # заповнюємо список
        self._res.config(text=self._pattern.format(count))  # виводимо результат


if __name__ == '__main__':
    test_top = Tk()
    test = GUI(test_top)
    test_top.mainloop()
