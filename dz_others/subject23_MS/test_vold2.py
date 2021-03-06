#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

# T23_21
# Р—Р»РёС‚С‚СЏ РґР°РЅРёС… Р· С„Р°Р№Р»С–РІ MS Word, MS Excel Р·Р° С€Р°Р±Р»РѕРЅРѕРј MS Word
# Р†РјРµРЅР° РїРѕР»С–РІ, С‰Рѕ Р·Р°РїРѕРІРЅСЋСЋС‚СЊСЃСЏ РґР°РЅРёРјРё, РјР°СЋС‚СЊ Р±СѓС‚Рё РІР·СЏС‚С– Сѓ С„С–РіСѓСЂРЅС– РґСѓР¶РєРё { }
# Р¤Р°Р№Р»Рё, Р· СЏРєРёС… С‚СЂРµР±Р° Р±СЂР°С‚Рё РґР°РЅС–, РІРєР°Р·СѓСЋС‚СЊ Сѓ РєРѕРЅС„С–РіСѓСЂР°С†С–Р№РЅРѕРјСѓ С„Р°Р№Р»С–
# РљР»Р°СЃ MergeSource

from openpyxl import *
from docx import Document
import os

from t23_22_sourceitem import *


class MergeSource:
    '''Р”Р¶РµСЂРµР»Р° РґР°РЅРёС… РґР»СЏ Р·Р»РёС‚С‚СЏ.

       РџСЂРёР·РЅР°С‡РµРЅРѕ РґР»СЏ РїС–Рґ'С”РґРЅР°РЅРЅСЏ РґРѕ РґР¶РµСЂРµР» РґР°РЅРёС… С‚Р° РїРѕРІРµСЂРЅРµРЅРЅСЏ РґР°РЅРёС… РїРѕ РєСЂРѕРєР°С….
       self.lead - С–Рј'СЏ РїРѕР»СЏ, СЏРєРµ С” РїСЂРѕРІС–РґРЅРёРј РїР°СЂР°РјРµС‚СЂРѕРј
       self.fields - СЃР»РѕРІРЅРёРє, С‰Рѕ РјР°С” РєР»СЋС‡Р°РјРё С–РјРµРЅР° РїРѕР»С–РІ, Р° Р·РЅР°С‡РµРЅРЅСЏРјРё -
                     РѕР±'С”РєС‚Рё РєР»Р°СЃСѓ SourceItem
       РљР»Р°СЃ РїС–РґС‚СЂРёРјСѓС” С–С‚РµСЂР°С†С–Р№РЅРёР№ РїСЂРѕС‚РѕРєРѕР».
    '''

    def __init__(self, param_files, leadparam):
        '''РљРѕРЅСЃС‚СЂСѓРєС‚РѕСЂ.

           Р—РґС–Р№СЃРЅСЋС” РїС–Рґ'С”РґРЅР°РЅРЅСЏ РґРѕ РґР¶РµСЂРµР» РґР°РЅРёС….
           param_files - СЃР»РѕРІРЅРёРє, С‰Рѕ РјС–СЃС‚РёС‚СЊ С–РјРµРЅР° РїР°СЂР°РјРµС‚СЂС–РІ (РїРѕР»С–РІ)
           С‚Р° С–РјРµРЅР° С„Р°Р№Р»С–РІ, РґРµ СЂРѕР·С‚Р°С€РѕРІР°РЅРѕ РІС–РґРїРѕРІС–РґРЅС– РґР°РЅС–.
           leadparam - РїСЂРѕРІС–РґРЅРёР№ РїР°СЂР°РјРµС‚СЂ.
           РљС–Р»СЊРєС–СЃС‚СЊ Р·Р°РїРёСЃС–РІ РґР°РЅРёС… СЂРѕР·СЂР°С…РѕРІСѓС”С‚СЊСЃСЏ Р·Р° С†РёРј РїР°СЂР°РјРµС‚СЂРѕРј.
        '''
        self.lead = leadparam
        self.fields = {}
        openfiles = {}  # СЃР»РѕРІРЅРёРє, С‰Рѕ РјС–СЃС‚РёС‚СЊ С„РјРµРЅР° С„Р°Р№Р»С–РІ С‚Р° РІС–РґРїРѕРІС–РґРЅС–
        # РѕР±'С”РєС‚Рё РґРѕРєСѓРјРµРЅС‚ (Document) Р°Р±Рѕ СЂРѕР±РѕС‡Р° РєРЅРёРіР° (Workbook)
        for name in param_files:
            filename = param_files[name]
            base, ext = os.path.splitext(filename)  # РІРёР·РЅР°С‡Р°С”РјРѕ С‚РёРї РґР¶РµСЂРµР»Р° РґР°РЅРёС…
            if ext == '.xlsx':
                typ = 'excel'
            else:
                typ = 'word'
            if filename not in openfiles:  # СЏРєС‰Рѕ С„Р°Р№Р» РЅРµ РІС–РґРєСЂРёС‚Рѕ, РІС–РґРєСЂРёРІР°С”РјРѕ
                # rootobj - С†Рµ РґРѕРєСѓРјРµРЅС‚ (Document) Р°Р±Рѕ СЂРѕР±РѕС‡Р° РєРЅРёРіР° (Workbook)
                if typ == 'excel':
                    rootobj = load_workbook(filename)
                else:
                    rootobj = Document(filename)
                openfiles[filename] = rootobj
            else:
                rootobj = openfiles[filename]
            islead = (name == leadparam)
            # СЃС‚РІРѕСЂСЋС”РјРѕ РЅРѕРІРёР№ РѕР±'С”РєС‚ SourceItem С‚Р° Р·Р°РїР°Рј'СЏС‚РѕРІСѓС”РјРѕ Сѓ СЃР»РѕРІРЅРёРєСѓ self.fields
            self.fields[name] = SourceItem(name, typ, rootobj, islead)

    def __iter__(self):
        '''РџРѕРІРµСЂС‚Р°С” РѕР±'С”РєС‚-С–С‚РµСЂР°С‚РѕСЂ.

           РњРµС‚РѕРґ РґР»СЏ РїС–РґС‚СЂРёРјРєРё С–С‚РµСЂР°С†С–Р№РЅРѕРіРѕ РїСЂРѕС‚РѕРєРѕР»Сѓ
        '''
        return self

    def __next__(self):
        '''РџРѕРІРµСЂС‚Р°С” РЅР°СЃС‚СѓРїРЅРёР№ Р·Р°РїРёСЃ Р· РґР°РЅРёРјРё РґР»СЏ Р·Р»РёС‚С‚СЏ.

           РњРµС‚РѕРґ РґР»СЏ РїС–РґС‚СЂРёРјРєРё С–С‚РµСЂР°С†С–Р№РЅРѕРіРѕ РїСЂРѕС‚РѕРєРѕР»Сѓ.
           Р—Р°РїРёСЃ - С†Рµ СЃР»РѕРІРЅРёРє Р· РєР»СЋС‡Р°РјРё-С–РјРµРЅР°РјРё РїРѕР»С–РІ С‚Р°
           Р·РЅР°С‡РµРЅРЅСЏРјРё - РѕР±'С”РєС‚Р°РјРё РєР»Р°СЃСѓ SourceItem.
        '''
        mergerecord = {}
        for name, srcitem in self.fields.items():
            # С‚СѓС‚ РјРѕР¶Рµ РІРёРЅРёРєРЅСѓС‚Рё РІРёРєР»СЋС‡РµРЅРЅСЏ StopIteration
            srcitem.next()  # РїРµСЂРµР№С‚Рё РґРѕ РЅР°СЃС‚СѓРїРЅРѕРіРѕ Р·Р°РїРёСЃСѓ
            mergerecord[name] = srcitem
        return mergerecord

