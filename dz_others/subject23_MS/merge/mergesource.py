#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from openpyxl import *
from docx import Document
import os

from dz_others.subject23_MS.merge.sourceitem import *


class MergeSource:

    def __init__(self, param_files, leadparam):
        self.lead = leadparam
        self.fields = {}
        openfiles = {}  # СЃР»РѕРІРЅРёРє, С‰Рѕ РјС–СЃС‚РёС‚СЊ С„РјРµРЅР° С„Р°Р№Р»С–РІ С‚Р° РІС–РґРїРѕРІС–РґРЅС–
        for name in param_files:
            filename = param_files[name]
            base, ext = os.path.splitext(filename)  # РІРёР·РЅР°С‡Р°С”РјРѕ С‚РёРї РґР¶РµСЂРµР»Р° РґР°РЅРёС…
            if ext == '.xlsx':
                typ = 'excel'
            else:
                typ = 'word'
            if filename not in openfiles:  # СЏРєС‰Рѕ С„Р°Р№Р» РЅРµ РІС–РґРєСЂРёС‚Рѕ, РІС–РґРєСЂРёРІР°С”РјРѕ
                if typ == 'excel':
                    rootobj = load_workbook(filename)
                else:
                    rootobj = Document(filename)
                openfiles[filename] = rootobj
            else:
                rootobj = openfiles[filename]
            islead = (name == leadparam)
            self.fields[name] = SourceItem(name, typ, rootobj, islead)

    def __iter__(self):
        return self

    def __next__(self):
        mergerecord = {}
        for name, srcitem in self.fields.items():
            srcitem.next()  # РїРµСЂРµР№С‚Рё РґРѕ РЅР°СЃС‚СѓРїРЅРѕРіРѕ Р·Р°РїРёСЃСѓ
            mergerecord[name] = srcitem
        return mergerecord

