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
        self.__is_loaned = is_loaned
        self._copies = copies
        self._genre = genre
        self._year = year


    def _setLoaned(self, input: bool) -> bool:
        """
        Sets if the book has been loaned or not
        """
        self.__loaned = input


    def _wasLoaned(self) -> bool:
        """
        Returns if the book was loaned or not.
        """
        return self.__loaned

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
