from abc import ABC, abstractmethod
import library
from database.book import Book

class __SearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str, field: str) -> list[Book]:
        responses= []
        for book in library.BOOKS:
            attribute= getattr(book, field)
            if query.lower() in attribute.lower():
                responses.append(book)
        return responses

class SearchByTitle(__SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'title')

class SearchByAuthor(__SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'author')

class SearchByCategory(__SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'genre')

class SearchByYear(__SearchStrategy):
    def search(self, query: str, books: list[Book]) -> list[Book]:
        return super().search(query, 'year')


class Search:
    def __init__(self, strategy: __SearchStrategy):
        self._strategy = strategy

    def execute_search(self, query: str) -> list[Book]:
        if not self._strategy:
            raise ValueError("Search strategy is not set.")
        return self._strategy.search(query, library.BOOKS)
