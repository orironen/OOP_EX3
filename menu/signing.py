from functools import partial
import tkinter as tk
import tkinter.messagebox as msgbox
import menu.baseGUI as gui
import menu.mainGUI as main

class LogInPage(gui.Page):
    """
    The page for logging into the library as a user.
    """
    def __init__(self):
        self.name= tk.Entry(main.ROOT, justify='left')
        self.passw= tk.Entry(main.ROOT, justify='left')
        super().__init__([
            gui.Element(tk.Label(main.ROOT, text="Welcome to the library!",
                                 height=3,
                                 font=("TkDefaultFont", 10)
                        ), 
                            {"row": 0, "column": 0, "padx": 2}),
            gui.Element(tk.Label(main.ROOT, text="Username",
                                 justify='right',
                                 anchor='e'
                                 ),
                        {"row": 1, "column": 0, "sticky": 'e'}),
            gui.Element(tk.Label(main.ROOT, text="Password",
                                 justify='right',
                                 anchor='e'
                                 ),
                        {"row": 2, "column": 0, "sticky": 'e'}),
            gui.Element(self.name,
                            {"row": 1, "column": 1, "padx": 1, "sticky": 'w'}),
            gui.Element(self.passw,
                            {"row": 2, "column": 1, "padx": 1, "sticky": 'w'}),
            gui.Element(tk.Button(main.ROOT, text="Log In",
                                  width=20,
                                  command= partial(self.login)
                        ),
                            {"row": 3, "column": 0, "columnspan": 2}),
            gui.Element(tk.Label(main.ROOT, text="Don't have an account?",
                                justify='right', 
                                anchor='e'
                                ),
                            {"row": 4, "column": 0, "sticky": 'e'}),
            gui.Element(tk.Button(main.ROOT, text="Register",
                                activeforeground="darkblue",
                                foreground="blue",
                                bd=0, 
                                justify='left', 
                                anchor='w', 
                                command=partial(main.WIN.switchToPage, "register")),
                            {"row": 4, "column": 1, "sticky": 'w'})
            ])
        
    def login(self):
        """
        Uses Library to help user enter main menu.
        """
        if main.LIB.logInUser(self.name.get(), self.passw.get()):
            msgbox.showinfo(title="Log In", message="Logged in successfully!")
        else:
            msgbox.showerror(title="Log In", message="Log in failed.")
        
class RegisterPage(gui.Page):
    """
    The page for registering to the library as a user.
    """
    def __init__(self):
        self.name= tk.Entry(main.ROOT, justify='left')
        self.passw= tk.Entry(main.ROOT, justify='left')
        super().__init__([
            gui.Element(tk.Label(main.ROOT, height=3, text="Register an account.", font=("TkDefaultFont", 10)),
                        {"row": 0, "column": 0, "padx": 2}),
            gui.Element(tk.Label(main.ROOT, text="Username",
                                 justify='right',
                                 anchor='e'
                                 ),
                        {"row": 1, "column": 0, "sticky": 'e'}),
            gui.Element(tk.Label(main.ROOT, text="Password",
                                 justify='right',
                                 anchor='e'
                                 ),
                        {"row": 2, "column": 0, "sticky": 'e'}),
            gui.Element(self.name,
                        {"row": 1, "column": 1, "padx": 1, "sticky": 'w'}),
            gui.Element(self.passw,
                        {"row": 2, "column": 1, "padx": 1, "sticky": 'w'}),
            gui.Element(tk.Button(main.ROOT, text="Register", width=20, command=partial(self.register)),
                        {"row": 3, "column": 0, "columnspan": 2}),
            gui.Element(tk.Label(main.ROOT, text="Already have an account?",
                                justify='right', 
                                anchor='e'
                                ),
                            {"row": 4, "column": 0, "sticky": 'e'}),
            gui.Element(tk.Button(main.ROOT, text="Log in",
                                activeforeground="darkblue",
                                foreground="blue",
                                bd=0, 
                                justify='left', 
                                anchor='w', 
                                command=partial(main.WIN.switchToPage, "log in")),
                            {"row": 4, "column": 1, "sticky": 'w'})
        ])

    def register(self):
        if main.LIB.registerUser(self.name.get(), self.passw.get()):
            msgbox.showinfo(title="Register", message=f"Registered successfully!")
            main.WIN.switchToPage("log in")
        else:
            msgbox.showerror(title="Register", message="Registration failed.")