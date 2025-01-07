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
        # לאורי:
        # private- "__[שם משתנה]"
        # protected- "_[שם משתנה]"
        pass

    @classmethod
    def update(cls, book: Self, details: list[str], newContent) -> Self:
        """
        Update one or more fields in the inputted Book object.
        """
        for detail in details:
            if detail != "is_loaned":
                detail= "_"+detail
            else:
                detail= "__"+detail
        attrs= ["_title", "_author", "__is_loaned", "_copies", "_genre", "_year"]
        for thing in attrs:
            if thing in details:
                setattr(book, thing, newContent)
        return book