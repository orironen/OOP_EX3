import tkinter as tk
from tkinter import ttk

class Element:
    """
    An element to be placed in a grid.
    """
    def __init__(self, wdgt: tk.Widget, kwarg: dict):
        self.widget= wdgt
        self.grid= kwarg

class Table:
    """
    A visual representation of a table in tkinter.
    """
    def __init__(self, root: tk.Tk, columns: tuple, content: list[list]):
        self.frame = ttk.Frame(root)
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', stretch=tk.YES)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        for item in content:
            tree.insert('', 'end', values=item)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
    def grid(self, kwargs: dict):
        """
        Place the table's frame in the grid.
        """
        self.frame.grid(kwargs)

    def grid_forget(self):
        """
        Remove the table's frame from the grid.
        """
        self.frame.grid_forget()

class Page:
    """
    A class representing one of the application's pages.
    """
    def __init__(self, elements: list[Element]):
        self.elements= elements

    def setElements(self):
        """
        Set the page elements in a grid.
        """
        for element in self.elements:
            element.widget.grid(element.grid)

    def hideElements(self):
        """
        Hide the page elements from view.
        """
        for element in self.elements:
            element.widget.grid_forget()

class MainWindow:
    """
    The main app window.
    """
    def __init__(self, root: tk.Tk):
        self.root= root
        self.current= None

    def initPages(self, pagemap: dict[str, Page]):
        """
        Initializes the pages the MainWindow will use.
        """
        self.pages= pagemap

    def refresh(self):
        """
        Refresh the booklist.
        """
        self.pages["view"].__init__()

    def switchToPage(self, newpagekey: str= None, newpage: Page= None):
        """
        Switches to the page via the inputted key.
        """
        # hide past page elements
        if self.current:
            self.current.hideElements()
        # set new page as current
        if newpagekey:
            self.current= self.pages[newpagekey]
        elif newpage:
            self.current= newpage
        else:
            raise ValueError
        self.current.setElements()
        # apply column weights
        for i in range(self.root.grid_size()[0]):
            self.root.columnconfigure(i, weight= 1)
        # set minimum window size
        self.root.update_idletasks()
        min_width= self.root.winfo_reqwidth()
        min_height= self.root.winfo_reqheight()
        self.root.minsize(min_width, min_height)
        # center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - min_width) // 2
        y = (screen_height - min_height) // 2
        self.root.geometry(f"{min_width}x{min_height}+{x}+{y}")

        self.root.mainloop()