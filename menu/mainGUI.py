from database.library import Library
import tkinter as tk
import menu.baseGUI as gui
import menu.signing as sign

LIB: Library
ROOT: tk.Tk
WIN: gui.MainWindow

def start_gui(library: Library):
    global LIB
    LIB= library
    global ROOT
    ROOT = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    ROOT.title('Library Database')
    global WIN
    WIN= gui.MainWindow(ROOT)
    WIN.initPages({
        "log in": sign.LogInPage(),
        "register": sign.RegisterPage()
    })
    WIN.switchToPage("log in")