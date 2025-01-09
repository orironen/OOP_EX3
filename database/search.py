from abc import ABC, abstractmethod
from copy import deepcopy
import database.library as library
from database.book import Book
from database.iterators import BookIterator

class SearchInterface(ABC):
    """
    Base interface for all search operations.
    """
    @abstractmethod
    def search(self, query: str, books: list[Book]) -> list[Book]:
        pass

class _SearchStrategy(SearchInterface):
    """
    Base class for the search implementation of the Strategy design pattern.
    """
    def search(self, query: str, books: list[Book], field: str) -> list[Book]:
        responses = []
        bookstack = BookIterator(books)
        while bookstack.hasNext():
            book = bookstack.next()
            attribute = getattr(book, field)
            if query.lower() in str(attribute).lower():
                responses.append(book)
        return responses

class SearchByTitle(_SearchStrategy):
    """
    Searches the book list by the book title.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, books, 'title')

class SearchByAuthor(_SearchStrategy):
    """
    Searches the book list by the author name.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, books, 'author')

class SearchByYear(_SearchStrategy):
    """
    Searches the book list by the release year.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, books, 'year')

class SearchDecorator(SearchInterface):
    """
    Base decorator that wraps a search component.
    """
    LIST: list[Book] = deepcopy(library.BOOKS)
    def __init__(self, search_component: SearchInterface):
        self._search = search_component

    def search(self, query: str, books: list[Book]) -> list[Book]:
        return self._search.search(query, books)

class AvailableDecorator(SearchDecorator):
    """
    Searches only available books.
    """
    def search(self, query: str) -> list[Book]:
        self.LIST = [book for book in self.LIST if not book.loaned]
        return self._search.search(query, self.LIST)

class LoanedDecorator(SearchDecorator):
    """
    Searches only loaned books.
    """
    def search(self, query: str) -> list[Book]:
        self.LIST = [book for book in self.LIST if book.loaned]
        return self._search.search(query, self.LIST)

class PopularDecorator(SearchDecorator):
    """
    Sorts search results based on book popularity.
    """
    def search(self, query: str) -> list[Book]:
        self.LIST.sort(key=lambda x: len(x.getWaitingList()), reverse=True)
        return self._search.search(query, self.LIST)

class AlphabeticalDecorator(SearchDecorator):
    """
    Sorts search results based on alphabetical order.
    """
    def search(self, query: str) -> list[Book]:
        self.LIST.sort(key=lambda x: x.title)
        return self._search.search(query, self.LIST)
    
class GenreDecorator(SearchDecorator):
    """
    Sorts search results based on genre.
    """
    def search(self, query: str) -> list[Book]:
        self.LIST.sort(key= lambda x: str(x.genre))
        return self._search.search(query, self.LIST)