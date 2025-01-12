import unittest
from database.library import Library
from database.book import BookFactory

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.test_book = BookFactory.create_book_from_input(
            "Test Book", "Test Author", "Fiction", "2023"
        )
    
    def test_add_book(self):
        initial_count = len(self.library.viewBooklist("all"))
        self.library.addBook(self.test_book)
        self.assertEqual(len(self.library.viewBooklist("all")), initial_count + 1)
    
    def test_remove_book(self):
        self.library.addBook(self.test_book)
        initial_count = len(self.library.viewBooklist("all"))
        self.library.removeBook(self.test_book)
        self.assertEqual(len(self.library.viewBooklist("all")), initial_count - 1)
    
    def test_borrow_book(self):
        self.library.addBook(self.test_book)
        self.library.borrowBook("test_user", self.test_book)
        self.assertIn(self.test_book, self.library.viewBooklist("loaned"))
    
    def test_return_book(self):
        self.library.addBook(self.test_book)
        self.library.borrowBook("test_user", self.test_book)
        self.library.returnBook("test_user", self.test_book)
        self.assertIn(self.test_book, self.library.viewBooklist("available"))