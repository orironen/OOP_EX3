import tkinter as tk
from tkinter import ttk
import menu.baseGUI as gui
import menu.mainGUI as main
from database.library import BOOKS

class ViewPage(gui.Page):
    """
    The page for viewing books.
    """
    def __init__(self, view: str):
        # select sorting option
        if view == "all":
            booklist= BOOKS
        elif view == "available":
            booklist= [book for book in BOOKS if not book.loaned]
        elif view == "loaned":
            booklist= [book for book in BOOKS if book.loaned]
        else:
            booklist= main.LIB.viewPopular()
        # create table
        table= gui.Table(main.ROOT, 
                  ("Title", "Author", "Is Loaned", "Copies", "Genre", "Year"),
                  [book.toList() for book in booklist])
        # initialize elements
        super().__init__([
            gui.Element(tk.Label(main.ROOT, text="View Books",
                                 height=3,
                                 font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0}),
            gui.Element(table.getFrame(),
                        {"row": 1, "column": 0, "sticky": "nsew"})
        ])