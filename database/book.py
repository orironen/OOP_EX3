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
        self.__loaned = is_loaned
        self._copies = copies
        self._genre = genre
        self._year = year
    
    def _setLoaned(self, input: bool) -> bool:
        """
        Sets if the book has been loaned or not
        """
        self.__loaned = input
    
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
            Book.__boolYesNo(self.__loaned),
            self._copies,
            str(self._genre),
            self._year
        ]

    @classmethod
    def parseBook(cls, l: list) -> Self:
        return Book(l[0], l[1], Book.__yesNoBool(l[2]), int(l[3]), Genre.parseGenre(l[4]), int(l[5]))