from copy import deepcopy
import book

class Library:
    """
    Represents a library database. Contains functions to manage books and users.
    """
    def __init__(self, books: list[book.Book], users):
        self.books= deepcopy(books)
        self.users= deepcopy(users)