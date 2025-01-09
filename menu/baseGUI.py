import tkinter as tk

class Element:
    """
    An element to be placed in a grid.
    """
    def __init__(self, wdgt: tk.Widget, kwarg: dict):
        self.widget= wdgt
        self.grid= kwarg

class Page:
    """
    A class representing one of the application's pages.
    """
    def __init__(self, elements: list[Element]):
        self.elements= elements

    def setElements(self):
        for element in self.elements:
            element.widget.grid(element.grid)

    def hideElements(self):
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

    def switchToPage(self, newpage: str):
        """
        Switches to the page via the inputted key.
        """
        # hide past page elements
        if self.current:
            self.current.hideElements()
        # set new page as current
        self.current= self.pages[newpage]
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