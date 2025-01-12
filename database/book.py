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
        self.borrowed= 0
        self.__waiting_list: list[str]= []

    def addToWaitingList(self, loaner: str):
        """
        Add a user to the book's waiting list.
        """
        self.__waiting_list.append(loaner)

    def removeFromWaitingList(self, loaner: str):
        """
        Clears the waiting list for the book.
        """
        self.__waiting_list.remove(loaner)

    def getWaitingList(self) -> list[str]:
        """
        Get a list of users waiting for the book.
        """
        return self.__waiting_list
    
    @classmethod
    def _yesNoBool(cls, string: str) -> bool:
        """
        Returns True if the string is 'Yes', False otherwise.
        """
        if string == 'Yes':
            return True
        return False

    @classmethod
    def _boolYesNo(cls, boolean: bool) -> str:
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
            Book._boolYesNo(self.loaned),
            self.copies,
            str(self.genre),
            self.year
        ]
    
    def __eq__(self, other: Self) -> bool:
        return self.title == other.title and self.author == other.author and str(self.genre) == str(other.genre) and self.year == other.year

class GenreBook(Book):
    """
    Base class for genre-specific books.
    """
    GENRE = None
    
    @classmethod
    def parseBook(cls, l: list) -> Self:
        """
        Parses a Book object out of the given list.
        """
        return cls(l[0], l[1], Book._yesNoBool(l[2]), int(l[3]), cls.GENRE, int(l[4]))

class FictionBook(GenreBook):
    GENRE = Genre.FICTION

class DystopianBook(GenreBook):
    GENRE = Genre.DYSTOPIAN

class ClassicBook(GenreBook):
    GENRE = Genre.CLASSIC

class AdventureBook(GenreBook):
    GENRE = Genre.ADVENTURE

class RomanceBook(GenreBook):
    GENRE = Genre.ROMANCE

class HistoricalFictionBook(GenreBook):
    GENRE = Genre.HISTORICAL_FICTION

class PsychologicalDramaBook(GenreBook):
    GENRE = Genre.PSYCHOLOGICAL_DRAMA

class PhilosophyBook(GenreBook):
    GENRE = Genre.PHILOSOPHY

class EpicPoetryBook(GenreBook):
    GENRE = Genre.EPIC_POETRY

class GothicFictionBook(GenreBook):
    GENRE = Genre.GOTHIC_FICTION

class GothicRomanceBook(GenreBook):
    GENRE = Genre.GOTHIC_ROMANCE

class RealismBook(GenreBook):
    GENRE = Genre.REALISM

class ModernismBook(GenreBook):
    GENRE = Genre.MODERNISM

class SatireBook(GenreBook):
    GENRE = Genre.SATIRE

class ScienceFictionBook(GenreBook):
    GENRE = Genre.SCIENCE_FICTION

class TragedyBook(GenreBook):
    GENRE = Genre.TRAGEDY

class FantasyBook(GenreBook):
    GENRE = Genre.FANTASY

class BookFactory:
    """
    Factory class for creating Book objects.
    """
    @staticmethod
    def create_book(title: str, author: str, is_loaned: str, copies: str, genre: Genre, year: str) -> Book:
        """
        Internal method for book creation.
        """
        genre_class_dict = {
            Genre.FICTION: FictionBook,
            Genre.DYSTOPIAN: DystopianBook,
            Genre.CLASSIC: ClassicBook,
            Genre.ADVENTURE: AdventureBook,
            Genre.ROMANCE: RomanceBook,
            Genre.HISTORICAL_FICTION: HistoricalFictionBook,
            Genre.PSYCHOLOGICAL_DRAMA: PsychologicalDramaBook,
            Genre.PHILOSOPHY: PhilosophyBook,
            Genre.EPIC_POETRY: EpicPoetryBook,
            Genre.GOTHIC_FICTION: GothicFictionBook,
            Genre.GOTHIC_ROMANCE: GothicRomanceBook,
            Genre.REALISM: RealismBook,
            Genre.MODERNISM: ModernismBook,
            Genre.SATIRE: SatireBook,
            Genre.SCIENCE_FICTION: ScienceFictionBook,
            Genre.TRAGEDY: TragedyBook,
            Genre.FANTASY: FantasyBook
        }
        return genre_class_dict[genre].parseBook([title, author, is_loaned, copies, year])

    @classmethod
    def create_book_from_input(cls, title: str, author: str, genre: str, year: str, is_loaned: str= "No", copies: str= 1) -> Book:
        """
        Create book from separate inputs.
        """
        genre = Genre.parseGenre(genre)
        return cls.create_book(title, author, is_loaned, copies, genre, year)

    @classmethod
    def create_book_from_row(cls, row: list) -> Book:
        """
        Create book from existing row.
        """
        genre = Genre.parseGenre(row[4])
        return cls.create_book(row[0], row[1], row[2], row[3], genre, row[5])