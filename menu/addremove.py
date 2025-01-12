from functools import partial
import tkinter as tk
import tkinter.messagebox as msgbox
from database.book import BookFactory
import menu.baseGUI as gui
import menu.mainGUI as main

class AddPage(gui.Page):
    """
    The page for adding new books.
    """
    def __init__(self):
        self.title= tk.Entry(main.ROOT, justify="left")
        self.author= tk.Entry(main.ROOT, justify="left")
        self.genre= tk.StringVar()
        self.genre.set("Fiction")
        genre_options = ["Fiction",
                         "Dystopian",
                         "Classic",
                         "Adventure",
                         "Romance",
                         "Historical Fiction",
                         "Psychological Drama",
                         "Philosophy",
                         "Epic Poetry",
                         "Gothic Fiction",
                         "Gothic Romance",
                         "Realism",
                         "Modernism",
                         "Satire",
                         "Science Fiction",
                         "Tragedy",
                         "Fantasy"
                        ]
        self.year= tk.Entry(main.ROOT, justify="left")
        super().__init__([
            gui.Element(tk.Label(main.ROOT, text="Add Books",
                                height=3,
                                font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0, "columnspan": 2}),
            gui.Element(tk.Label(main.ROOT, text="The following book will be added to the list of available books.\nYou cannot add books to the list of loaned books."),
                        {"row": 1, "column": 0, "columnspan": 2}),
            gui.Element(tk.Label(main.ROOT, text="Title",
                                 justify="right",
                                 anchor="e"),
                        {"row": 2, "column": 0, "sticky": "e"}),
            gui.Element(self.title,
                        {"row": 2, "column": 1, "sticky": "w"}),
            gui.Element(tk.Label(main.ROOT, text="Author",
                                 justify="right",
                                 anchor="e"),
                        {"row": 3, "column": 0, "sticky": "e"}),
            gui.Element(self.author,
                        {"row": 3, "column": 1, "sticky": "w"}),
            gui.Element(tk.Label(main.ROOT, text="Genre",
                                 justify="right",
                                 anchor="e"),
                        {"row": 4, "column": 0, "sticky": "e"}),
            gui.Element(tk.OptionMenu(main.ROOT, self.genre, *genre_options),
                        {"row": 4, "column": 1, "sticky": "w"}),
            gui.Element(tk.Label(main.ROOT, text="Year",
                                 justify="right",
                                 anchor="e"),
                        {"row": 5, "column": 0, "sticky": "e"}),
            gui.Element(self.year,
                        {"row": 5, "column": 1, "sticky": "w"}),
            gui.Element(tk.Button(main.ROOT, text="Add",
                                  width= 20,
                                  command=partial(self.addBook)),
                        {"row": 6, "column": 0, "columnspan": 2}),
            gui.Element(tk.Button(main.ROOT, text= "Back",
                                  command=partial(main.WIN.switchToPage, "main")),
                        {"row": 7, "column": 0, "columnspan": 2})
                        ])
        
    def addBook(self):
        try:
            main.LIB.addBook(BookFactory.create_book_from_input(self.title.get(), self.author.get(), self.genre.get(), self.year.get()))
            msgbox.showinfo(title="Add Book", message=f"{self.title.get()} added successfully.")
        except OSError:
            msgbox.showerror(title="Add Book", message=f"Could not add {self.title}.")
            