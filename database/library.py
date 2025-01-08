from copy import deepcopy
import csv
import random
import string
import hashlib
import shutil
from abc import ABC, abstractmethod
from Users.user import User
from database.book import Book
import database.strategies as strategies
from database.iterators import UserIterator

BOOKS: list[Book] = []
AVAILABLE_BOOKS: list[Book] = []
LOANED_BOOKS: list[Book] = []
USERS: list[User] = []

def _csvAsMatrix(file: str) -> list:
    """
    Returns a matrix representing the rows of the csv file.
    """
    with open(file, 'r', newline='') as f:
        return list(csv.reader(f, delimiter=','))

def _ifFileExists(file: str) -> bool:
    """
    Returns True if file path exists, False otherwise.
    """
    try:
        with open(file, 'r'):
            pass
    except OSError:
        return False
    return True

class _Obserable(ABC):
    @abstractmethod
    def notify(self, message: str):
        """
        Notify the inputted message to all observers.
        """
        pass

class Library(_Obserable):
    """
    Represents a library database. Contains functions to manage books and users.
    """
    def __init__(self):
        # get books from csv
        with open('books.csv', 'r', newline='') as bookfile:
            booklist = csv.reader(bookfile, delimiter=',')
            for i, row in enumerate(booklist):
                if i != 0:
                    BOOKS.append(Book.parseBook(row))
        # copy into available books
        if not _ifFileExists('available_books.csv'):
            AVAILABLE_BOOKS.extend(book for book in BOOKS if not book._wasLoaned())
            with open('available_books.csv', 'x', newline='') as bookfile:
                writer= csv.writer(bookfile, delimiter=',')
                writer.writerow(["title","author","is_loaned","copies","genre","year"])
                writer.writerows(book.toList() for book in AVAILABLE_BOOKS)
        if not _ifFileExists('loaned_books.csv'):
            LOANED_BOOKS.extend(book for book in BOOKS if book._wasLoaned())
            with open('loaned_books.csv', 'x', newline='') as bookfile:
                writer= csv.writer(bookfile, delimiter=',')
                writer.writerow(["title","author","is_loaned","copies","genre","year"])
                writer.writerows(book.toList() for book in LOANED_BOOKS)
        if not _ifFileExists('log.txt'):
            with open('log.txt', 'x') as log:
                log.write('')

    def __log__(self, action: str):
        """
        Logs an action into the log file.
        """
        with open('log.txt', 'a') as log:
            log.write(f'{action}\n')

    def __addBookToCSV(self, book: Book, csvfile: str):
        """
        Internal method to add a book to the given csvfile path.
        """
        with open(csvfile, 'a', newline='') as books:
            booklist = csv.writer(books, delimiter=',')
            booklist.writerow(book.toList())

    def addBook(self, book: Book):
        """
        Adds a book to the library.
        """
        BOOKS.append(book)
        AVAILABLE_BOOKS.append(book)
        try:
            # add new book to csv
            self.__addBookToCSV(book, 'books.csv')
            self.__addBookToCSV(book, 'available_books.csv')
            self.__log__('book added successfully')
        except OSError:
            self.__log__('book added fail')

    def __removeBookFromCSV(self, book: Book, csvfile: str):
        """
        Internal method to remove a book from the given csvfile path.
        """
        # read csv
        bookfile= _csvAsMatrix(csvfile)
        # remove relevant row
        rows= [row for row in bookfile if row[0] == book._title]
        # write to csv
        with open(csvfile, 'w', newline='') as books:
            bookwriter= csv.writer(books)
            bookwriter.writerows(rows)

    def removeBook(self, book: Book):
        """
        Removes a book from the library.
        """
        BOOKS.remove(book)
        AVAILABLE_BOOKS.remove(book)
        try:
            self.__removeBookFromCSV(book, 'books.csv')
            self.__removeBookFromCSV(book, 'available_books.csv')
            self.__log__('book removed successfully')
        except OSError:
            self.__log__('book removed fail')

    def updateBookDetails(self, oldBook: Book, newBook: Book, csvfile: str):
        """
        Updates the details of the book in the specified index in the
        specified CSV file.
        """
        BOOKS[BOOKS.index(oldBook)]= newBook
        AVAILABLE_BOOKS[AVAILABLE_BOOKS.index(oldBook)]= newBook
        # read csv
        bookfile= _csvAsMatrix(csvfile)
        # update relevant row 
        rows= [newBook.toList() if oldBook._title == row[0] else row for row in bookfile]
        # write to csv
        with open(csvfile, 'w', newline='') as books:
            bookwriter= csv.writer(books)
            bookwriter.writerows(rows)

    def registerUser(self, name: str, password: str) -> User:
        """
        Register a user to the library.
        """
        # generate random salt
        salt= ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        # create user
        newuser= User(name, hashlib.sha256((password+salt).encode()), salt)
        USERS.append(newuser)
        if not _ifFileExists('users.csv'):
            with open('users.csv', 'x') as userfile:
                userwriter= csv.writer(userfile, delimiter=',')
                userwriter.writerow(["name","password","salt"])
        try:
            with open('users.csv', 'a') as userfile:
                userwriter= csv.writer(userfile, delimiter=',')
                userwriter.writerow([name, password, salt])
            self.__log__("registered successfully")
            return newuser
        except OSError:
            self.__log__("registered fail")

    def logInUser(self, username: str, password: str) -> bool:
        """
        Returns True if the password matches the username.
        """
        userIter= UserIterator()
        while userIter.hasNext():
            user= userIter.next()
            if user.name == username:
                current= user
        if current.passwordMatch(password):
            self.__log__('logged in successfully')
            return True
        else:
            self.__log__('logged in fail')
            return False
        
    def borrowBook(self, bookname: str):
        """
        Borrows a book from the library in the name of the
        mentioned user.
        """
        try:
            # find book in available
            booksearch= strategies.Search(strategies.SearchByTitle())
            book_to_borrow= deepcopy(booksearch.execute_search(bookname, AVAILABLE_BOOKS)[0])
            backup= deepcopy(book_to_borrow)
            # update book
            book_to_borrow._copies-=1
            book_to_borrow._setLoaned(True)
            # update available books
            self.updateBookDetails(backup, book_to_borrow, 'available_books.csv')
            # find book in loaned
            try:
                loaned_book= deepcopy(booksearch.execute_search(bookname, LOANED_BOOKS)[0])
                # update loaned books
                backup= deepcopy(loaned_book)
                loaned_book._copies+=1
                self.updateBookDetails(backup, loaned_book, 'loaned_books.csv')
            except IndexError:
                book_to_borrow._copies= 1
                self.__addBookToCSV(book_to_borrow, 'loaned_books.csv')
        except OSError:
            self.__log__('book borrowed fail')

    def returnBook(self, bookname: str):
        """
        Borrows a book from the library in the name of the
        mentioned user.
        """
        try:
            # find book in available
            booksearch= strategies.Search(strategies.SearchByTitle())
            book_to_return= deepcopy(booksearch.execute_search(bookname, LOANED_BOOKS)[0])
            backup= deepcopy(book_to_return)
            # update book
            book_to_return._copies-=1
            book_to_return._setLoaned(False)
            # update available books
            self.updateBookDetails(backup, book_to_return, 'loaned_books.csv')
            # find book in loaned
            try:
                returned_book= deepcopy(booksearch.execute_search(bookname, AVAILABLE_BOOKS)[0])
                # update loaned books
                backup= deepcopy(returned_book)
                returned_book._copies+=1
                self.updateBookDetails(backup, returned_book, 'available_books.csv')
            except IndexError:
                book_to_return._copies= 1
                self.__addBookToCSV(book_to_return, 'available_books.csv')
        except OSError:
            self.__log__('book borrowed fail')

    def notify(self, message: str):
        for observer in USERS:
            observer.update(message)