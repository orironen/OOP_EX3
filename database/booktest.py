import unittest
from book import BookFactory, Genre, Book, FictionBook, RomanceBook

class TestBookFactory(unittest.TestCase):
    def test_create_book_from_input(self):
        book = BookFactory.create_book_from_input(
            "Title", "Author", "Fiction", "2023"
        )
        self.assertIsInstance(book, FictionBook)
        self.assertEqual(book.genre, Genre.FICTION)
    
    def test_create_book_from_row(self):
        row = ["Title", "Author", "No", "1", "Romance", "2023"]
        book = BookFactory.create_book_from_row(row)
        self.assertIsInstance(book, RomanceBook)
        self.assertEqual(book.genre, Genre.ROMANCE)
    
    def test_invalid_genre_creation(self):
        with self.assertRaises(ValueError):
            BookFactory.create_book_from_input(
                "Title", "Author", "Invalid Genre", "2023"
            )

class TestGenre(unittest.TestCase):
    def test_genre_string_conversion(self):
        self.assertEqual(str(Genre.HISTORICAL_FICTION), "Historical Fiction")
        self.assertEqual(str(Genre.SCIENCE_FICTION), "Science Fiction")
    
    def test_genre_parsing(self):
        self.assertEqual(Genre.parseGenre("Historical Fiction"), Genre.HISTORICAL_FICTION)
        self.assertEqual(Genre.parseGenre("Science Fiction"), Genre.SCIENCE_FICTION)
    
    def test_invalid_genre_parsing(self):
        with self.assertRaises(ValueError):
            Genre.parseGenre("Invalid Genre")            

class TestBook(unittest.TestCase):
    def setUp(self):
        self.book = Book("Test Title", "Test Author", False, 1, Genre.FICTION, 2023)
    
    def test_waiting_list(self):
        self.book.addToWaitingList("user1")
        self.assertEqual(self.book.getWaitingList(), ["user1"])
        
        self.book.removeFromWaitingList("user1")
        self.assertEqual(self.book.getWaitingList(), [])
    
    def test_bool_conversion(self):
        self.assertTrue(Book._yesNoBool("Yes"))
        self.assertFalse(Book._yesNoBool("No"))
        
        self.assertEqual(Book._boolYesNo(True), "Yes")
        self.assertEqual(Book._boolYesNo(False), "No")
    
    def test_to_list(self):
        expected = ["Test Title", "Test Author", "No", 1, "Fiction", 2023]
        self.assertEqual(self.book.toList(), expected)

class TestGenreBook(unittest.TestCase):
    def test_fiction_book_creation(self):
        book_data = ["Title", "Author", "No", "1", "2023"]
        fiction_book = FictionBook.parseBook(book_data)
        
        self.assertEqual(fiction_book.title, "Title")
        self.assertEqual(fiction_book.genre, Genre.FICTION)
    
    def test_genre_mismatch(self):
        # Test that a FictionBook can't be created with non-fiction genre data
        book_data = ["Title", "Author", "No", "1", Genre.ROMANCE, "2023"]
        with self.assertRaises(ValueError):
            FictionBook.parseBook(book_data)

