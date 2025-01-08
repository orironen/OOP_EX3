from enum import Enum, auto
from typing import Self

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
        self._title = title
        self._author = author
        self._loaned = is_loaned
        self._copies = copies
        self._genre = genre
        self._year = year

    def _setLoaned(self, input: bool) -> bool:
        """
        Sets if the book has been loaned or not.
        """
        self._loaned = input

    def _wasLoaned(self) -> bool:
        """
        Returns if the book was loaned or not.
        """
        return self._loaned
    
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
            self._title,
            self._author,
            Book.__boolYesNo(self._loaned),
            self._copies,
            str(self._genre),
            self._year
        ]

    @classmethod
    def parseBook(cls, l: list) -> Self:
        """
        Parses a Book object out of the given list.
        """
        return Book(l[0], l[1], Book.__yesNoBool(l[2]), int(l[3]), Genre.parseGenre(l[4]), int(l[5]))

class BookFactory:
    @staticmethod
    def create_book(data: dict) -> Book:
            return Book(
                title=data["title"],
                author=data["author"],
                is_loaned=data["is_loaned"],
                copies=data["copies"],
                genre=Genre.parseGenre(data["genre"]),
                year=data["year"],
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

class AvailableBook(BookDecorator):

    def is_available(self) -> bool:
        return not self.isLoaned()

class BorrowedBookDecorator(BookDecorator):
    def is_borrowed(self) -> bool:
        return self._book._is_loaned()