import sqlite3


class dbManager:

    def __init__(self):
        self.conn = sqlite3.connect('shelf.db')
        self.curs = self.conn.cursor()

    def removeRecord(self, record: tuple):
        q = """DELETE FROM editions 
                WHERE name=? AND authors=? AND genre=? AND type=? AND date=? AND place=?"""
        self.curs.execute(q, record)
        self.conn.commit()

    def addRecord(self, record: tuple):
        q = "INSERT INTO editions VALUES(?, ?, ?, ?, ?, ?)"
        self.curs.execute(q, record)
        self.conn.commit()

    def searchBy(self, keyword, searchType):
        _map = {
            "On name": "SELECT * FROM editions WHERE name LIKE '%' || ? || '%'",
            "On author": "SELECT * FROM editions WHERE authors LIKE '%' || ? || '%'",
            "On genre": "SELECT * FROM editions WHERE genre LIKE '%' || ? || '%'",
            "On type": "SELECT * FROM editions WHERE type LIKE '%' || ? ||'%'",
            "On date": "SELECT * FROM editions WHERE date LIKE '%' || ? || '%'",
            "On place": "SELECT * FROM editions WHERE place LIKE '%' || ? || '%'",
            "List all": "SELECT * FROM editions"
        }
        q = _map[searchType]
        if not searchType == "List all":
            self.curs.execute(q, (keyword,))
        else:
            self.curs.execute(q)
        res = self.curs.fetchall()
        return res
