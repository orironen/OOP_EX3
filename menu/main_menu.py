import tkinter as tk

def main():
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    root.title('Library Database')

    # create sign in elements
    welcomelabel = tk.Label(root, height=3, text="Welcome to the library!", font=("TkDefaultFont", 10))
    namelabel= tk.Label(root, text="Username")
    passlabel= tk.Label(root, text="Password")
    nameentry= tk.Entry(root)
    passentry= tk.Entry(root)
    signinbutt= tk.Button(root, text="Sign In", width=20)

    # grid
    welcomelabel.grid(row=0, column=0, padx=2)
    namelabel.grid(row=1, column=0)
    nameentry.grid(row=1, column=1, padx=1)
    passlabel.grid(row=2, column=0)
    passentry.grid(row=2, column=1, padx=1)
    signinbutt.grid(row=3, column=0, columnspan=2)
    root.mainloop()