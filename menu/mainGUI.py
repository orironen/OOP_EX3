from functools import partial
from database.library import Library
import tkinter as tk
import tkinter.messagebox as msgbox
import menu.addremove as add
import menu.viewing as view
import menu.baseGUI as gui
import menu.signing as sign

LIB: Library
ROOT: tk.Tk
WIN: gui.MainWindow

class MainPage(gui.Page):
    """
    The main menu. Has access to every library function.
    """
    def __init__(self):
        super().__init__([
            gui.Element(tk.Label(ROOT, text="Main Menu",
                                 height=3,
                                 font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0, "columnspan": 3}),
            gui.Element(tk.Button(ROOT, text="View Books",
                                  width=20,
                                  command=partial(WIN.switchToPage, "view")),
                        {"row": 1, "column": 0}),
            gui.Element(tk.Button(ROOT, text="Add Book",
                                  width=20,
                                  command=partial(WIN.switchToPage, "add")),
                        {"row": 1, "column": 1}),
            gui.Element(tk.Button(ROOT, text="Remove Book",
                                  width=20),
                        {"row": 1, "column": 2}),
            gui.Element(tk.Button(ROOT, text="Search Books",
                                  width=20,
                                  command=partial(WIN.switchToPage, "search")),
                        {"row": 2, "column": 0}),
            gui.Element(tk.Button(ROOT, text="Lend Book",
                                  width=20),
                        {"row": 2, "column": 1}),
            gui.Element(tk.Button(ROOT, text="Return Book",
                                  width=20),
                        {"row": 2, "column": 2}),
            gui.Element(tk.Button(ROOT, text="Log Out",
                                activeforeground="darkblue",
                                foreground="blue",
                                bd=0,
                                command=partial(self.logout)),
                        {"row": 3, "column": 0, "columnspan": 3})
        ])
    
    def logout(self):
        """
        Asks whether you want to log out. If confirmed, returns to the login page.
        """
        confirm= msgbox.askokcancel("Log Out", "Are you sure you want to log out?")
        if confirm:
            LIB.logOutUser()
            WIN.switchToPage("log in")

def start_gui(library: Library):
    """
    Starts the database GUI.
    """
    global LIB
    LIB= library
    global ROOT
    ROOT = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    ROOT.title('Library Database')
    global WIN
    WIN= gui.MainWindow(ROOT)
    WIN.initPages({
        "log in": sign.LogInPage(),
        "register": sign.RegisterPage(),
        "main": MainPage(),
        "view": view.ViewPage(),
        "search": view.SearchEntryPage(),
        "add": add.AddPage()
    })
    WIN.switchToPage("log in")