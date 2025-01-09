from functools import partial
import tkinter as tk
import tkinter.messagebox as msgbox
import menu.baseGUI as gui
import menu.mainGUI as main

def login(username: str, password: str):
    """
    Uses Library to help user enter main menu.
    """
    if main.LIB.logInUser(username, password):
        msgbox.showinfo(title="Log In", message="Logged in successfully!")
    else:
        msgbox.showerror(title="Log In", message="Log in failed.")

def register(username: str, password: str):
    if main.LIB.registerUser(username, password):
        msgbox.showinfo(title="Register", message="Registered successfully!")
        main.WIN.switchToPage("log in")
    else:
        msgbox.showerror(title="Register", message="Registration failed.")

class LogInPage(gui.Page):
    """
    The page for logging into the library as a user.
    """
    def __init__(self):
        nameentry= tk.Entry(main.ROOT)
        passentry= tk.Entry(main.ROOT)
        super().__init__([
            gui.Element(tk.Label(main.ROOT, text="Welcome to the library!",
                                 height=3,
                                 font=("TkDefaultFont", 10)
                        ), 
                            {"row": 0, "column": 0, "padx": 2}),
            gui.Element(tk.Label(main.ROOT, text="Username"),
                            {"row": 1, "column": 0}),
            gui.Element(tk.Label(main.ROOT, text="Password"),
                            {"row": 2, "column": 0,}),
            gui.Element(nameentry,
                            {"row": 1, "column": 1, "padx": 1}),
            gui.Element(passentry,
                            {"row": 2, "column": 1, "padx": 1}),
            gui.Element(tk.Button(main.ROOT, text="Log In",
                                  width=20,
                                  command= partial(login, nameentry.get(), passentry.get())
                        ),
                            {"row": 3, "column": 0, "columnspan": 2}),
            gui.Element(tk.Label(main.ROOT, text="Don't have an account?"),
                            {"row": 4, "column": 0}),
            gui.Element(tk.Button(main.ROOT, text="Register",
                                activeforeground="lightblue",
                                foreground="blue",
                                bd=0, 
                                justify='left', 
                                anchor='w', 
                                command=partial(main.WIN.switchToPage, "register")),
                            {"row": 4, "column": 1, "sticky": 'w'})
            ])
        
class RegisterPage(gui.Page):
    """
    The page for registering to the library as a user.
    """
    def __init__(self):
        nameentry= tk.Entry(main.ROOT)
        passentry= tk.Entry(main.ROOT)
        super().__init__([
            gui.Element(tk.Label(main.ROOT, height=3, text="Register an account.", font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0, "padx": 2}),
            gui.Element(tk.Label(main.ROOT, text="Username"),
                        {"row": 1, "column": 0}),
            gui.Element(tk.Label(main.ROOT, text="Password"),
                        {"row": 2, "column": 0}),
            gui.Element(nameentry,
                        {"row": 1, "column": 1, "padx": 1}),
            gui.Element(passentry,
                        {"row": 2, "column": 1, "padx": 1}),
            gui.Element(tk.Button(main.ROOT, text="Register", width=20, command=partial(register, nameentry.get(), passentry.get())),
                        {"row": 3, "column": 0, "columnspan": 2})
        ])