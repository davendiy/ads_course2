from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math_projects.bookshelf.dbmanager as dbmanager


class GUI:

    def __init__(self):
        self.root = Tk()
        self.dbMngr = dbmanager.dbManager()
        self.root.title("Home library manager")
        self.root.geometry("800x600")
        self.mainPg = EditionsManager(self.root, self)
        self.mainPg.pack()
        self.frames = {}
        mainloop()


class EditionsManager(Frame):
    """
    Overall initialization scheme:

    __init__ -> initLayout -> configNotebook -> initSearchTab -> initTreeView
                                            |                |-> Entries, buttons, etc.
                                            |                |-> link handler of 'Transfer to edit page' button
                                            |                |-> link handler of 'Remove' button
                                            |                |-> link handler of 'Go' button
                                            |                |-> link handler of choice made in drop-down menu
                                            |
                                            |-> initAddTab -> link 'Proceed' button
                                            |
                                            |-> initEditTab -> link 'Commit' button

    """

    def __init__(self, parent, app):
        Frame.__init__(self, parent)
        # buffer for database record which is needed to compare 'initial value of record' with 'edited value of record'
        # as comparison itself is divided into two separate methods, some kind of 'buffer' required
        self.buffer = None
        self.app = app  # application instance, to able to reach database manager
        self.initLayout()  # main layout configuration method

    def initLayout(self):
        title = ttk.Label(self, text="Editions Manager")
        title.pack(padx=10, pady=10, anchor='center')
        self._configNotebook()

    def _configNotebook(self):
        """
        Helper function, here notebook configuration implemented

        :return:
        """
        options = [
            "On name",
            "On author",
            "On date",
            "On genre",
            "On type",
            "List all"
        ]
        # notebook with tabs for different purposes (search, add, edit)
        self.nb = ttk.Notebook(self, width=750, height=500)
        self.nb.pack()
        self.nbTabs = tuple([ttk.Frame(self) for _ in range(3)])  # frames for notebook tabs
        aliases = ("Search", "Add", "Edit")  # notebook tabs aliases
        for p, n in zip(self.nbTabs, aliases):  # tabs initialization
            self.nb.add(p, text=n, padding=2)
        subFr1 = ttk.Frame(self.nbTabs[0])  # sub frame for "Search" tab
        subFr1.pack()
        self._initSearchTab(subFr1, options)  # init and config "Search" tab
        subFr2 = ttk.Frame(self.nbTabs[1])  # sub frame for "Add" tab
        subFr2.pack(side='left', padx=40, pady=40, anchor=NW)
        self._initAddTab(subFr2)  # init and config "Add" tab
        subFr3 = ttk.Frame(self.nbTabs[2])  # sub frame for "Edit" tab
        subFr3.pack(side='left', padx=40, pady=40, anchor=NW)
        self._initEditTab(subFr3)  # init and config "Edit" tab

    def _initSearchTab(self, ancestor, options):
        """
        Helper method to init 'Search' tab

        :param ancestor: ancestor frame
        :param options: list of options to be added into drop down menu
        :return:
        """
        lb2 = ttk.Label(ancestor, text="Search Keyword")
        lb2.grid(row=0, column=0, padx=10, pady=5)
        self.searchEntry = ttk.Entry(ancestor)
        self.searchEntry.grid(row=0, column=1)
        but = ttk.Button(ancestor, text="Go", command=self.processChoice)
        self.choiceVar = StringVar(ancestor)  # choice variable associated with drop down menu
        lb = ttk.Label(ancestor, text="Search Type")
        lb.grid(row=0, column=2, padx=10, pady=5)
        om = ttk.OptionMenu(ancestor, self.choiceVar, "", *options)
        om.config(width=10)
        om.grid(row=0, column=3, padx=10, pady=5)
        but.grid(row=0, column=4)
        self._initTreeView(ancestor)
        but2 = ttk.Button(ancestor, text="Transfer to edit page", command=self._handleEdit)
        but3 = ttk.Button(ancestor, text="Remove", command=self._handleRemove)
        but2.grid(row=2, column=0)
        but3.grid(row=2, column=1)

    def _initTreeView(self, ancestor):
        """
        Helper method to init and config tree view widget, with it we will display result of
        our query to database
        """
        # tree view and scroll widgets, linkage one to another
        self.tv = ttk.Treeview(ancestor, show="headings")
        self.scrl = ttk.Scrollbar(ancestor, command=self.tv.yview)
        self.tv.configure(yscrollcommand=self.scrl.set)
        self.tv.configure(height=18)
        # column heads name assignment
        heads = ("Name", "Authors", "Genre", "Type", "Date", "Place")
        self.tv["columns"] = heads
        for h in heads:
            self.tv.column(h, width=100, anchor="center")
            self.tv.heading(h, text=h, anchor="center")
        self.tv.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=20)
        self.scrl.grid(row=1, column=6, sticky="nsew", pady=20)

    def _initAddTab(self, ancestor):
        """Helper method to init 'Add' tab"""
        self.einsAdd = []  # list of entries on Add tab, we'll need it to make a query to database
        for i in range(6):
            ein = ttk.Entry(ancestor, width=20)
            ein.grid(row=i, column=1, pady=5)
            self.einsAdd.append(ein)
        names = ("Name", "Authors", "Genre", "Type", "Date", "Place")  # labels names
        for i, n in enumerate(names):
            lb = ttk.Label(ancestor, text=n)
            lb.grid(row=i, column=0)
        but = ttk.Button(ancestor, text="Proceed", command=self._handleProceed)
        but.grid(row=7, column=2, padx=10, pady=10)

    def _initEditTab(self, ancestor):
        """Helper method to init 'Edit' tab"""
        self.einsEdit = []  # list of entries on Edit tab, we'll need it to make a query to database
        for i in range(6):
            ein = ttk.Entry(ancestor, width=20)
            ein.grid(row=i, column=1, pady=5)
            self.einsEdit.append(ein)
        names = ("Name", "Authors", "Genre", "Type", "Date", "Place")
        for i, n in enumerate(names):
            lb = ttk.Label(ancestor, text=n)
            lb.grid(row=i, column=0, pady=5)
        but = ttk.Button(ancestor, text="Commit changes", command=self._handleCommit)
        but.grid(row=7, column=2, padx=10, pady=10)

    def _handleEdit(self):
        """Button 'Transfer to Edit page' press event handler"""
        for e in self.einsEdit:
            e.delete(0, END)
        item = self.tv.focus()  # get selected item from tree view
        oldRecord = tuple(self.tv.item(item)["values"])  # get required data from item
        for i, e in enumerate(self.einsEdit):
            e.insert(0, oldRecord[i])  # fill entries on EDIT tab
        edFrm = self.nbTabs[2]
        self.nb.select(edFrm)  # switch to EDIT tab
        # variable to transfer previous state of record further (it will be needed in COMMIT meth)
        self.buffer = oldRecord

    def _handleCommit(self):
        """Button 'Commit' press event handler"""
        old = self.buffer
        self.buffer = None
        new = []
        for e in self.einsEdit:
            new.append(e.get())
        if all([s == '' for s in new]):  # avoid empty entries case
            messagebox.showinfo("Record edition", "Full-empty record are not allowed")
        new = tuple(new)  # build a new record
        self.app.dbMngr.removeRecord(old)  # remove old record
        self.app.dbMngr.addRecord(new)  # add new record
        messagebox.showinfo("Record edition", "Record was edited successfully")
        for e in self.einsEdit:  # clear entries
            e.delete(0, END)

    def _handleProceed(self):
        """Button 'Proceed' press event handler"""
        data = []
        for en in self.einsAdd:
            data.append(en.get())  # collect data from entries
        if all([s == '' for s in data]):
            messagebox.showinfo("Record addition", "At least one value needed!")
            return
        for i in range(len(data)):  # replace empty strings with NULL
            if not data[i]:
                data[i] = "NULL"
        s = "The next record will be added to db: {}\nProceed?"
        flag = messagebox.askyesno("Record addition", s.format(", ".join(data)))
        if flag:
            self.app.dbMngr.addRecord(tuple(data))  # perform and "Add record" query to data base
            messagebox.showinfo("Record addition", "Record added successfully!")
            for e in self.einsEdit:  # clear entries
                e.delete(0, END)

    def _handleRemove(self):
        """Button 'Remove' press event handler"""
        item = self.tv.focus()  # get selected item from tree view
        record = tuple(self.tv.item(item)['values'])  # get required data from selected item, build record
        if record:
            flag = messagebox.askyesno("Book removal",
                                       "Are you sure you want to remove selected book?: {}".format(repr(record)))
            if flag:
                self.app.dbMngr.removeRecord(record)  # ask for record removal
                messagebox.showinfo("Book removal", "Book was removed successfully")

    def processChoice(self):
        """Handles choices made in option menu"""
        self.tv.delete(*self.tv.get_children())  # clear tree view
        searchType = self.choiceVar.get()
        keyword = self.searchEntry.get()
        data = self.app.dbMngr.searchBy(keyword, searchType)
        for rec in data:
            self._insertInTv(rec)

    def _insertInTv(self, record: tuple):
        """Insert record in tree view"""
        if len(record) > 6:
            return
        self.tv.insert("", "end", values=record)


if __name__ == '__main__':
    g = GUI()
