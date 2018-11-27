#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import tkinter as tk


class Block:
    """ Реалізація графічного інтерфейсу
    """

    def __init__(self, master):
        """ Ініціалізація

        :param master: об'єкт, до якого буде прив'язаний інтерфейс
        """
        self.entry = tk.Entry(master, width=50, font=("arial", '20'))  # поле введення
        self.butt = tk.Button(master, text='Обробити', font=("arial", '20'))
        self.lab = tk.Label(master, text='Вивід', font=("arial", '20'))

        self.entry.pack(side=tk.TOP)
        self.lab.pack(fill=tk.Y)
        self.butt.pack()

    def choose_func(self, text_func: str):
        """ Вибір функції, яка буде застосовуватись до рядка
        """
        self.butt['command'] = self.__getattribute__(text_func)

    def amount_diff(self):
        """ Рахує к-ть змін знаку

        """
        s = self.entry.get().split(', ')
        if not s:
            return
        count = 0
        current = s[0]
        for el in s:
            if int(el) * int(current) < 0:
                count += 1
            current = el
        self.lab['text'] = str(count)


if __name__ == '__main__':
    root = tk.Tk()
    test1 = Block(root)
    test1.choose_func('amount_diff')

    root.mainloop()
