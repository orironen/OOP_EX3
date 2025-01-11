from abc import ABC, abstractmethod
from database.book import Book
from database.iterators import BookIterator

class _BooklistStrategy(ABC):
    """
    Base interface for all strategies.
    """
    def __init__(self, books: list[Book]):
        self.books= books

class _ViewStrategy(_BooklistStrategy):
    """
    Base interface for all viewing operations.
    """
    @abstractmethod
    def view(self) -> list[Book]:
        """
        Views the booklist.
        """
        pass

class _SearchInterface(_BooklistStrategy):
    """
    Base interface for all search operations.
    """
    @abstractmethod
    def search(self, query: str) -> list[Book]:
        """
        Searches the booklist based on the query.
        """
        pass

class _SearchStrategy(_SearchInterface):
    """
    Base class for a search implementation of the Strategy design pattern.
    """
    def search(self, query: str, field: str) -> list[Book]:
        responses = []
        bookstack = BookIterator(self.books)
        while bookstack.hasNext():
            book = bookstack.next()
            attribute = getattr(book, field)
            if query.lower() in str(attribute).lower():
                responses.append(book)
        return responses

class ViewBooklist(_ViewStrategy):
    """
    Strategy design pattern for viewing the booklist.
    """
    def view(self) -> list[Book]:
        return self.books

class SearchByTitle(_SearchStrategy):
    """
    Searches the book list by the book title.
    """
    def search(self, query: str) -> list[Book]:
        return super().search(query, 'title')

class SearchByAuthor(_SearchStrategy):
    """
    Searches the book list by the author name.
    """
    def search(self, query: str) -> list[Book]:
        return super().search(query, 'author')
    
class SearchByGenre(_SearchStrategy):
    """
    Searches the book list by the book genre.
    """
    def search(self, query: str) -> list[Book]:
        return super().search(query, 'genre')

class SearchByYear(_SearchStrategy):
    """
    Searches the book list by the release year.
    """
    def search(self, query: str) -> list[Book]:
        return super().search(query, 'year')

class BooklistDecorator(_SearchInterface, _ViewStrategy):
    """
    Base decorator that wraps a search component.
    """
    def __init__(self, component: _BooklistStrategy):
        self._comp = component

    def view(self):
        return self._comp.books

    def search(self, query: str) -> list[Book]:
        return self._comp.search(query, self._comp.books)

class AvailableDecorator(BooklistDecorator):
    """
    Views only available books.
    """
    def view(self):
        return [book for book in self._comp.books if not book.loaned]
    
    def search(self, query: str) -> list[Book]:
        sorted_books = [book for book in self._comp.books if not book.loaned]
        return self._comp.search(query, sorted_books)

class LoanedDecorator(BooklistDecorator):
    """
    Views only loaned books.
    """
    def view(self):
        return [book for book in self._comp.books if book.loaned]
    
    def search(self, query: str) -> list[Book]:
        sorted_books = [book for book in self._comp.books if book.loaned]
        return self._comp.search(query, sorted_books)

class PopularDecorator(BooklistDecorator):
    """
    Sorts list based on book popularity.
    """
    def view(self):
        return sorted(self._comp.books, key=lambda x: x.borrowed, reverse=True)

    def search(self, query: str) -> list[Book]:
        sorted_books= sorted(self._comp.books, key=lambda x: x.borrowed, reverse=True)[:10]
        return self._comp.search(query, sorted_books)

class AlphabeticalDecorator(BooklistDecorator):
    """
    Sorts results based on alphabetical order.
    """
    def view(self):
        return sorted(self._comp.books, key=lambda x: x.title)
    
    def search(self, query: str) -> list[Book]:
        sorted_books= sorted(self._comp.books, key=lambda x: x.title)
        return self._comp.search(query, sorted_books)
    
class GenreDecorator(BooklistDecorator):
    """
    Sorts results based on genre.
    """
    def view(self):
        return sorted(self._comp.books, key= lambda x: str(x.genre))
    
    def search(self, query: str) -> list[Book]:
        sorted_books= sorted(self._comp.books, key= lambda x: str(x.genre))
        return self._comp.search(query, sorted_books)