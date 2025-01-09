from functools import partial
import tkinter as tk
from database.library import Library

LIB: Library
ROOT: tk.Tk

class UserSign:
    def __init__(self):
        self.elements= []

    def addElements(self, elmts: list):
        self.elements.extend(elmts)

    def register(self):
        for element in self.elements:
            element.destroy()
        self.elements.clear()
        # create register elements
        reglabel = tk.Label(ROOT, height=3, text="Register an account.", font=("TkDefaultFont", 10))
        namelabel= tk.Label(ROOT, text="Username")
        passlabel= tk.Label(ROOT, text="Password")
        nameentry= tk.Entry(ROOT)
        passentry= tk.Entry(ROOT)
        regbutt= tk.Button(ROOT, text="Register", width=20, command=partial(LIB.registerUser, nameentry.get(), passentry.get()))

        # grid
        reglabel.grid(row=0, column=0, padx=2)
        namelabel.grid(row=1, column=0)
        nameentry.grid(row=1, column=1, padx=1)
        passlabel.grid(row=2, column=0)
        passentry.grid(row=2, column=1, padx=1)
        regbutt.grid(row=3, column=0, columnspan=2)
        self.addElements([reglabel, namelabel, passlabel, nameentry, passentry, regbutt])
        ROOT.mainloop()

    def sign_in(self):
        global ROOT
        ROOT = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
        ROOT.title('Library Database')

        # create sign in elements
        welcomelabel = tk.Label(ROOT, height=3, text="Welcome to the library!", font=("TkDefaultFont", 10))
        namelabel= tk.Label(ROOT, text="Username")
        passlabel= tk.Label(ROOT, text="Password")
        nameentry= tk.Entry(ROOT)
        passentry= tk.Entry(ROOT)
        signinbutt= tk.Button(ROOT, text="Sign In", width=20, command=LIB.logInUser(nameentry.get(), passentry.get()))
        reglabel= tk.Label(ROOT, text="Don't have an account?")
        regbutt= tk.Button(ROOT, text="Register", foreground="blue", bd=0, justify='left', anchor='w', command=partial(self.register))

        # grid
        welcomelabel.grid(row=0, column=0, padx=2)
        namelabel.grid(row=1, column=0)
        nameentry.grid(row=1, column=1, padx=1)
        passlabel.grid(row=2, column=0)
        passentry.grid(row=2, column=1, padx=1)
        signinbutt.grid(row=3, column=0, columnspan=2)
        reglabel.grid(row=4, column=0)
        regbutt.grid(row=4, column=1, sticky='w')
        self.addElements([welcomelabel, namelabel, passlabel, nameentry, passentry, signinbutt, reglabel, regbutt])
        ROOT.mainloop()

def start_gui(library: Library):
    global LIB
    LIB= library
    signing= UserSign()
    signing.sign_in()