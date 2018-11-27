#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 27.11.18
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


from tkinter import *
from tkinter.messagebox import *


class DoubleList:

    def __init__(self, master, list_all, list_sel=None):
        self.top = master
        self._list_sel = list(list_sel) if list_sel else []
        self._list_all = list(set(list_all) - set(list_sel))
        self._list_sel.sort()
        self._list_all.sort()
        self._cancel = False

        self._make_widgets()

    def _make_widgets(self):
        self._flist_all = Frame(self.top)
        self._sb_all = Scrollbar(self._flist_all)
        self._sb_all.pack(side=RIGHT, fill=Y)
        self._l_all = Listbox(self._flist_all, height=15,
                              width=50, yscrollcommand=self._sb_all.set)
        self._sb_all.config(command=self._l_all.yview)
        self._l_all.pack(side=RIGHT, fill=BOTH, expand=YES)
        self._flist_all.pack(side=LEFT, fill=Y, expand=YES)

        self._l_all.bind('<Double-1>', self._right_handler)

        self._fill_list(self._list_all, self._l_all)

        self._fbut = Frame(self.top)
        self._b_right = Button(self._fbut, text='   >>   ',
                               command=self._right_handler)
        self._b_left = Button(self._fbut, text='   <<   ',
                              command=self._left_handler)
        self._b_right.pack(side=TOP, padx=5, pady=5)
        self._b_left.pack(side=TOP, padx=5, pady=5)
        self._fbut.pack(side=LEFT, fill=Y, expand=YES)

        self._flist_sel = Frame(self.top)
        self._sb_sel = Scrollbar(self._flist_sel)
        self._sb_sel.pack(side=RIGHT, fill=Y)
        self._l_sel = Listbox(self._flist_sel, height=15,
                              width=50, yscrollcommand=self._sb_sel.set)
        self._sb_sel.config(command=self._l_sel.yview)
        self._l_sel.pack(side=RIGHT, fill=BOTH, expand=YES)
        self._flist_sel.pack(side=LEFT, fill=Y, expand=YES)

        self._l_sel.bind('<Double-1>', self._left_handler)

        self._fill_list(self._list_sel, self._l_sel)

        self.bfm = Frame(self.top)
        self.bok = Button(self.bfm, text='      Ok      ',
                          command=self.ok_handler)
        self.bcancel = Button(self.bfm,
                              text='Р’С–РґРјС–РЅРёС‚Рё',
                              command=self.cancel_handler)
        self.bok.pack(side=TOP, padx=5, pady=5)
        self.bcancel.pack(side=TOP, padx=5, pady=5)
        self.bfm.pack(side=LEFT, fill=Y, expand=YES)

    def _fill_list(self, items, lst):
        lst.delete(0, END)  # РѕС‡РёСЃС‚РёС‚Рё СЃРїРёСЃРѕРє РЅР° РµРєСЂР°РЅС–
        for item in items:
            lst.insert(END, item)

    def _right_handler(self, ev=None):
        try:
            cur_sel = self._l_all.curselection()
            elem = self._l_all.get(cur_sel)
            if not elem:
                return
            index = cur_sel[0]
            # РѕРЅРѕРІРёС‚Рё СЃРїРёСЃРѕРє
            self._l_all.delete(index)
            self._l_sel.insert(END, self._list_all[index])
            self._list_sel.append(self._list_all[index])
            del self._list_all[index]
        except TclError:
            pass
        except Exception as e:
            showwarning('РџРѕРјРёР»РєР°', e)

    def _left_handler(self, ev=None):
        try:
            # РѕС‚СЂРёРјР°С‚Рё РІРёР±СЂР°РЅРёР№ РµР»РµРјРµРЅС‚ СЃРїРёСЃРєСѓ
            cur_sel = self._l_sel.curselection()
            elem = self._l_sel.get(cur_sel)
            if not elem:
                return
            index = cur_sel[0]
            # РѕРЅРѕРІРёС‚Рё СЃРїРёСЃРѕРє
            self._l_sel.delete(index)
            self._l_all.insert(END, self._list_sel[index])
            self._list_all.append(self._list_sel[index])
            del self._list_sel[index]
        except TclError:
            # РїСЂРѕРїСѓСЃС‚РёС‚Рё РїРѕРјРёР»РєСѓ curselection, СЏРєС‰Рѕ РїС–Рґ С‡Р°СЃ
            # РїРѕРґРІС–Р№РЅРѕРіРѕ РЅР°С‚РёСЃРЅРµРЅРЅСЏ Р»С–РІРѕС— РєР»Р°РІС–С€С– РјРёС€С– СЃРїРёСЃРѕРє РїРѕСЂРѕР¶РЅС–Р№
            pass
        except Exception as e:
            # СЏРєС‰Рѕ С–РЅС€Р° РїРѕРјРёР»РєР°, С‚Рѕ РІРёРґР°С‚Рё РїРѕРІС–РґРѕРјР»РµРЅРЅСЏ
            showwarning('РџРѕРјРёР»РєР°', e)

    def ok_handler(self, ev=None):
        self.top.destroy()  # Р·Р°РєСЂРёС‚Рё РІС–РєРЅРѕ self.top

    def cancel_handler(self, ev=None):
        self._cancel = True
        self.ok_handler(ev)

    def get(self):
        result = self._list_sel if not self._cancel else None
        return result


def main():
    top = Tk()
    d = DoubleList(top, range(10), range(2, 5))
    mainloop()
    sel = d.get()
    print(sel)


if __name__ == '__main__':
    main()
