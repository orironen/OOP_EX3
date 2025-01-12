from functools import partial
import tkinter as tk
import menu.baseGUI as gui
import menu.mainGUI as main

class ViewPage(gui.Page):
    """
    The page for viewing books.
    """
    def __init__(self, view: str= "all", sort: str= "abc", booklist: list= None):
        # select sorting option
        booklist= main.LIB.viewBooklist(view, booklist)
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
    
    @classmethod
    def changeView(cls, view: str, sort: str):
        """
        Changes the ViewPage's view.
        """
        main.WIN.switchToPage(newpage=ViewPage(view, sort))

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

class SearchEntryPage(gui.Page):
    """
    The page for searching for books based on their properties.
    """
    def __init__(self):
        self.query= tk.Entry(main.ROOT)
        self.searchby= tk.StringVar()
        self.searchby.set("Title")
        super().__init__([gui.Element(tk.Label(main.ROOT, text="Search Books",
                                 height=3,
                                 font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0, "columnspan": 2}),
                        gui.Element(self.query,
                        {"row": 1, "column": 0}),
                        gui.Element(tk.OptionMenu(main.ROOT, self.searchby,
                                                  "Title",
                                                  "Author",
                                                  "Genre",
                                                  "Year"),
                                    {"row": 1, "column": 1}),
                        gui.Element(tk.Button(main.ROOT, text= "Search",
                                              width= 20,
                                              command= partial(self.search)),
                                    {"row": 2, "column": 0, "columnspan": 2}),
                        gui.Element(tk.Button(main.ROOT, text= "Back",
                                            command=partial(main.WIN.switchToPage, "main")),
                                    {"row": 3, "column": 0, "columnspan": 2})
                        ])
    
    def search(self):
        """
        Search for the query inputted in the page, based on the factors given
        to it.
        """
        booklist= main.LIB.searchBooklist(self.query.get(), self.searchby.get())
        main.WIN.switchToPage(newpage= ViewPage(booklist=booklist))