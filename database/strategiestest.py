import unittest
from database.strategies import SearchByTitle, SearchByAuthor, SearchByGenre
from database.book import Book, Genre

class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book("Test Book", "John Doe", False, 1, Genre.FICTION, 2023),
            Book("Another Book", "Jane Smith", False, 1, Genre.ROMANCE, 2022)
        ]
    
    def test_search_by_title(self):
        strategy = SearchByTitle(self.books)
        results = strategy.search("Test")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Test Book")
    
    def test_search_by_author(self):
        strategy = SearchByAuthor(self.books)
        results = strategy.search("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "John Doe")
    
    def test_search_by_genre(self):
        strategy = SearchByGenre(self.books)
        results = strategy.search("Fiction")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].genre, Genre.FICTION)