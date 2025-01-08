from abc import ABC, abstractmethod
import database.library as library
from database.book import Book

class _SearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str, field: str, books: list[Book]) -> list[Book]:
        responses= []
        for book in books:
            attribute= getattr(book, field)
            if query.lower() in attribute.lower():
                responses.append(book)
        return responses

class SearchByTitle(_SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'title', books)

class SearchByAuthor(_SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'author', books)

class SearchByCategory(_SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'genre', books)

class SearchByYear(_SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'year', books)

class Search:
    def __init__(self, strategy: _SearchStrategy):
        self._strategy = strategy

    def execute_search(self, query: str, books: list[Book]) -> list[Book]:
        if not self._strategy:
            raise ValueError("Search strategy is not set.")
        return self._strategy.search(query, books)
