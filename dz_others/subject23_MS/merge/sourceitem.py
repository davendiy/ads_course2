#!/usr/bin/env python3
# -*-encoding: utf-8-*-


class SourceItem:
    def __init__(self, field, typ, rootobject, islead=False):
        self.type = typ
        self.rootobj = rootobject
        self.islead = islead
        self.obj = None
        if self.type == 'excel':
            self._findexcel(field)
        else:
            self._findword(field)

    def _findexcel(self, field):
        found = False
        for sheet in self.rootobj:
            r = sheet.min_row  # РЅРѕРјРµСЂ СЂСЏРґРєР°, Р· СЏРєРѕРіРѕ РїРѕС‡РёРЅР°СЋС‚СЊСЃСЏ РґР°РЅС– РІ Р°СЂРєСѓС€С–
            for c in range(sheet.min_column, sheet.max_column + 1):
                if str(sheet.cell(row=r, column=c).value) == field:
                    found = True
                    break
            if found: break
        if not found:
            raise ValueError  # change
        self.parent = sheet
        self.row = r
        self.col = c

    def _findword(self, field):
        found = False
        for table in self.rootobj.tables:
            for c, cell in enumerate(table.row_cells(0)):
                if cell.text == field:
                    found = True
                    break
            if found: break
        if not found:
            raise ValueError  # change
        # РІСЃС‚Р°РЅРѕРІР»СЋС”РјРѕ Р·РЅР°С‡РµРЅРЅСЏ РґР»СЏ Р·РЅР°Р№РґРµРЅРѕРіРѕ РґР¶РµСЂРµР»Р° РґР°РЅРёС…
        self.parent = table
        self.row = 0
        self.col = c

    def next(self):
        self.row += 1
        if self.type == 'excel':
            if self.row > self.parent.max_row:  # СЏРєС‰Рѕ РІРёС…РѕРґРёРјРѕ Р·Р° РјРµР¶С– РѕР±Р»Р°СЃС‚С– РґР°РЅРёС…
                if self.islead:
                    raise StopIteration
                else:
                    self.row = self.parent.min_row + 1
            self.obj = self.parent.cell(row=self.row, column=self.col)
        else:
            if self.row >= len(self.parent.rows):  # СЏРєС‰Рѕ РІРёС…РѕРґРёРјРѕ Р·Р° РјРµР¶С– РѕР±Р»Р°СЃС‚С– РґР°РЅРёС…
                if self.islead:
                    raise StopIteration
                else:
                    self.row = 1
            self.obj = self.parent.cell(self.row, self.col)
