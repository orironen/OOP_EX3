from abc import ABC, abstractmethod
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
    
class SearchByGenre(_SearchStrategy):
    """
    Searches the book list by the book genre.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, books, 'genre')

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
    def __init__(self, search_component: SearchInterface):
        self._search = search_component

    def search(self, query: str, books: list[Book]) -> list[Book]:
        return self._search.search(query, books)

class AvailableDecorator(SearchDecorator):
    """
    Searches only available books.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        sorted_books = [book for book in books if not book.loaned]
        return self._search.search(query, sorted_books)

class LoanedDecorator(SearchDecorator):
    """
    Searches only loaned books.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        sorted_books = [book for book in books if book.loaned]
        return self._search.search(query, sorted_books)

class PopularDecorator(SearchDecorator):
    """
    Sorts search results based on book popularity.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        sorted_books= sorted(books, key=lambda x: x.borrowed, reverse=True)
        return self._search.search(query, sorted_books)

class AlphabeticalDecorator(SearchDecorator):
    """
    Sorts search results based on alphabetical order.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        sorted_books= sorted(books, key=lambda x: x.title)
        return self._search.search(query, sorted_books)
    
class GenreDecorator(SearchDecorator):
    """
    Sorts search results based on genre.
    """
    def search(self, query: str, books: list[Book]) -> list[Book]:
        sorted_books= sorted(books, key= lambda x: str(x.genre))
        return self._search.search(query, sorted_books)