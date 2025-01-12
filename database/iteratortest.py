import unittest
from database.iterators import BookIterator, UserIterator
from database.book import Book, Genre
from Users.user import User

class TestIterators(unittest.TestCase):
    def setUp(self):
        self.books = [
            Book("Test1", "Author1", False, 1, Genre.FICTION, 2023),
            Book("Test2", "Author2", False, 1, Genre.ROMANCE, 2023)
        ]
        self.users = [
            User("Test1", "pass1", "salt1"),
            User("Test2", "pass2", "salt2")
        ]
        
    def test_book_iterator(self):
        iterator = BookIterator(self.books)
        self.assertTrue(iterator.hasNext())
        self.assertEqual(iterator.next().title, "Test1")
        self.assertTrue(iterator.hasNext())
        self.assertEqual(iterator.next().title, "Test2")
        self.assertFalse(iterator.hasNext())
        with self.assertRaises(IndexError):
            iterator.next()

    def test_user_iterator(self):
        iterator = UserIterator(self.users)
        self.assertTrue(iterator.hasNext())
        self.assertEqual(iterator.next().name, "Test1")
        self.assertTrue(iterator.hasNext())
        self.assertEqual(iterator.next().name, "Test2")
        self.assertFalse(iterator.hasNext())