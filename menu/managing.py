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
        """
        Use library method to add a book with the data provided.
        """
        try:
            main.LIB.addBook(BookFactory.create_book_from_input(self.title.get(), self.author.get(), self.genre.get(), self.year.get()))
            main.WIN.refresh()
            msgbox.showinfo(title="Add Book", message=f"{self.title.get()} added successfully. Book may not appear to be added initially.")
        except OSError:
            msgbox.showerror(title="Add Book", message=f"Could not add {self.title.get()}.")

class ChoosePage(gui.Page):
    """
    A page where you select a book.
    """
    def __init__(self, title: str, desc: str, butt: str, loaned: bool= False):
        if loaned:
            self.booklist= main.LIB.viewBooklist("loaned")
        else:
            self.booklist= main.LIB.viewBooklist("available")
        self.selected= tk.StringVar()
        self.selected.set("Choose Book")
        super().__init__([
            gui.Element(tk.Label(main.ROOT, text=title,
                                height=3,
                                font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0}),
            gui.Element(tk.Label(main.ROOT, text=desc),
                        {"row": 1, "column": 0}),
            gui.Element(tk.OptionMenu(main.ROOT, self.selected,
                                      *[book.title for book in self.booklist]),
                        {"row": 2, "column": 0}),
            gui.Element(tk.Button(main.ROOT, text=butt,
                                  command=partial(self.command)),
                        {"row": 3, "column": 0}),
            gui.Element(tk.Button(main.ROOT, text= "Back",
                                  command=partial(main.WIN.switchToPage, "main")),
                        {"row": 4, "column": 0})
        ])
    
    def command(self):
        """
        Execute the given page's command.
        """
        pass

class RemovePage(ChoosePage):
    """
    The page for removing books.
    """
    def __init__(self):
        desc= """You can only remove books from the available booklist."""
        super().__init__("Remove Books", desc, "Remove")

    def command(self):
        try:
            book= [book for book in self.booklist if book.title == self.selected.get()][0]
            main.LIB.removeBook(book)
            main.WIN.refresh()
            msgbox.showinfo(title="Remove Book", message=f"{book.title} removed successfully. Book may not appear to be removed initially.")
        except:
            msgbox.showerror(title="Remove Book", message=f"Could not remove {book.title}.")