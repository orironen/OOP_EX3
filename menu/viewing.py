from functools import partial
import tkinter as tk
import menu.baseGUI as gui
import menu.mainGUI as main

class ViewPage(gui.Page):
    """
    The page for viewing books.
    """
    def __init__(self, view: str= "all", sort: str= "abc"):
        # select sorting option
        if view == "all":
            booklist= main.LIB.viewAll()
        elif view == "available":
            booklist= main.LIB.viewAvailable()
        elif view == "loaned":
            booklist= main.LIB.viewLoaned()
        elif view == "popular":
            booklist= main.LIB.viewPopular()
        if sort == "abc":
            booklist= main.LIB.sortByTitle(booklist)
        elif sort == "genre":
            booklist= main.LIB.sortByGenre(booklist)
        self.view= view
        self.sort= sort
        # create table
        table= gui.Table(main.ROOT, 
                  ("Title", "Author", "Is Loaned", "Copies", "Genre", "Year"),
                  [book.toList() for book in booklist])
        main.ROOT.grid_rowconfigure(1, weight=1)
        # initialize elements
        super().__init__([
            gui.Element(tk.Label(main.ROOT, text="View Books",
                                 height=3,
                                 font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0}),
            gui.Element(table,
                        {"row": 1, "column": 0, "sticky": "nsew"}),
            gui.Element(tk.Button(main.ROOT, text= "Back",
                                  command=partial(main.WIN.switchToPage, "main")),
                        {"row": 2, "column": 0})
        ])

    def setElements(self):
        menu= tk.Menu(main.ROOT)
        main.ROOT.config(menu=menu)
        # view menu
        viewmenu= tk.Menu(menu)
        menu.add_cascade(label='View', menu=viewmenu)
        viewmenu.add_command(label='All', command=partial(self.changeView, "all", self.sort))
        viewmenu.add_command(label='Available', command=partial(self.changeView, "available", self.sort))
        viewmenu.add_command(label='Loaned', command=partial(self.changeView, "loaned", self.sort))
        viewmenu.add_command(label='Popular', command=partial(self.changeView, "popular", self.sort))
        # sort menu
        sortmenu= tk.Menu(menu)
        menu.add_cascade(label='Sort by...', menu=sortmenu)
        sortmenu.add_command(label='Title', command=partial(self.changeView, self.view, "abc"))
        sortmenu.add_command(label='Genre', command=partial(self.changeView, self.view, "genre"))
        super().setElements()

    def hideElements(self):
        main.ROOT.config(menu="")
        super().hideElements()

    def changeView(self, view: str, sort: str):
        """
        Changes the ViewPage's view.
        """
        main.WIN.switchToPage(newpage=ViewPage(view, sort))