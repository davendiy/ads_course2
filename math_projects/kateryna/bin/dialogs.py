#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo, showerror

from .database import *
from .constants import *


class DialogChangeSite:

    def __init__(self, pre, default: dict, item_type=SITE):
        self.pre = pre
        self.default = default
        self._type = item_type
        if item_type == SITE:
            self._fields = SITES_DATA_FIELDS
        else:
            self._fields = KEY_WORDS_DATA_FIELDS

        self.diag = Toplevel()
        self.diag.focus_set()
        self._widgets = {}
        self._make_widgets()

    def _make_widgets(self):
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
        if askyesno('Warning', 'Do you really want to delete this {}?'.format(self._type[:-1])):
            try:
                database.del_item(item_type=self._type, item_id=self.default['Id'])
                showinfo('Successful', 'Item is successfully updated.')
            except Exception as e:
                showerror('Error', e)
                logging.exception(e)
            self.diag.destroy()
