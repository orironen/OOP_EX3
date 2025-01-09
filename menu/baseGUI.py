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

    def destroyElements(self):
        for element in self.elements:
            element.widget.destroy()

class MainWindow:
    """
    The main app window.
    """
    def __init__(self, root: tk.Tk):
        self.root= root
        self.current= None

    def initPages(self, pagemap: dict[str, Page]):
        self.pages= pagemap

    def switchToPage(self, newpage: str):
        if self.current:
            self.current.destroyElements()
        self.current= self.pages[newpage]
        self.current.setElements()
        self.root.mainloop()