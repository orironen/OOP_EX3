from enum import Enum, auto
from typing import Self

from Users.user import User

class Genre(Enum):
    """
    An enum representing all the genres listed in the books.csv.
    """
    FICTION = auto()
    DYSTOPIAN = auto()
    CLASSIC = auto()
    ADVENTURE = auto()
    ROMANCE = auto()
    HISTORICAL_FICTION = auto()
    PSYCHOLOGICAL_DRAMA = auto()
    PHILOSOPHY = auto()
    EPIC_POETRY = auto()
    GOTHIC_FICTION = auto()
    GOTHIC_ROMANCE = auto()
    REALISM = auto()
    MODERNISM = auto()
    SATIRE = auto()
    SCIENCE_FICTION = auto()
    TRAGEDY = auto()
    FANTASY = auto()

    def __str__(self):
        return self.name.replace('_', ' ').title()

    @classmethod
    def parseGenre(cls, obj: str) -> Self:
        """
        A method that parses a string into a Genre object.
        """
        for genre in Genre:
            if genre.__str__() == obj:
                return genre
        raise ValueError(f"No genre matching '{obj}' found")

class Book:
    """
    A class representing a book. Contains the title, genre,
    author, year, and other info.
    """
    def __init__(self, title: str, author: str, is_loaned: bool, copies: int, genre: Genre, year: int):
        self.title = title
        self.author = author
        self.loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.__waiting_list: list[User]= []

    def addToWaitingList(self, user: User):
        """
        Add a user to the book's waiting list.
        """
        self.__waiting_list.append(user)

    def removeFromWaitingList(self, user: User):
        """
        Clears the waiting list for the book.
        """
        self.__waiting_list.remove(user)

    def getWaitingList(self) -> list[User]:
        """
        Get a list of users waiting for the book.
        """
        return self.__waiting_list
    
    @classmethod
    def __yesNoBool(cls, string: str) -> bool:
        """
        Returns True if the string is 'Yes', False otherwise.
        """
        if string == 'Yes':
            return True
        return False

    @classmethod
    def __boolYesNo(cls, boolean: bool) -> str:
        """
        Returns 'Yes' if the boolean is True, 'No' otherwise.
        """
        if boolean:
            return 'Yes'
        return 'No'

    def toList(self) -> list[str]:
        """
        Returns a list object of all the book's fields.
        """
        return [
            self.title,
            self.author,
            Book.__boolYesNo(self.loaned),
            self.copies,
            str(self.genre),
            self.year
        ]

    @classmethod
    def parseBook(cls, l: list) -> Self:
        """
        Parses a Book object out of the given list.
        """
        return Book(l[0], l[1], Book.__yesNoBool(l[2]), int(l[3]), Genre.parseGenre(l[4]), int(l[5]))

class BookFactory:
    @staticmethod
    def create_book(title: str, author: str, is_loaned: bool, copies: int, genre: str, year: int) -> Book:
        return Book(
            title=title,
            author=author,
            is_loaned=is_loaned,
            copies=copies,
            genre=Genre.parseGenre(genre),
            year=year,
        )

class BookDecorator:
    """
    Base class for decorating a Book object.
    """
    def __init__(self, book: Book):
        self._book = book

    def __getattr__(self, name):
        return getattr(self._book, name)

class popularBook(BookDecorator):
    def __init__(self, book: Book):
        super().__init__(book)
        self.waiting_list = []

    def add_to_waiting_list(self, user: str):
        if self.isLoaned():
            self.waiting_list.append(user)

    def get_waiting_list(self):
        return self.waiting_list

class availableBook(BookDecorator):

    def is_available(self) -> bool:
        return not self.isLoaned()

class borrowedBook(BookDecorator):
    def is_borrowed(self) -> bool:
        return self._book._is_loaned()