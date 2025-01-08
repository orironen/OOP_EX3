from copy import deepcopy
import csv
import random
import string
import hashlib
from Users.user import User
from book import Book, Genre
from database.iterators import UserIterator

BOOKS: list[Book] = []
_USERS: list[User] = []

def __csvAsMatrix(file: str) -> list:
    """
    Returns a matrix representing the rows of the csv file.
    """
    with open(file, 'r', newline='') as f:
        return list(csv.reader(f, delimiter=','))

def __ifFileExists(file: str) -> bool:
    """
    Returns True if file path exists, False otherwise.
    """
    try:
        with open(file, 'r'):
            pass
    except OSError:
        return False
    return True

def __yesNoBool(string: str) -> bool:
    """
    Returns True if the string is 'Yes', False otherwise.
    """
    if string == 'Yes':
        return True
    return False

def __boolYesNo(boolean: bool) -> str:
    """
    Returns 'Yes' if the boolean is True, 'No' otherwise.
    """
    if boolean:
        return 'Yes'
    return 'No'

class Library:
    """
    Represents a library database. Contains functions to manage books and users.
    """
    def __init__(self, users: list[User]):
        # get books from csv
        with open('books.csv', 'r', newline='') as books:
            booklist = csv.reader(books, delimiter=',')
            for row in booklist:
                BOOKS.append(Book(
                    row[0], 
                    row[1], 
                    __yesNoBool(row[2]), 
                    int(row[3]), 
                    Genre.parseGenre(row[4]), 
                    int(row[5])
                ))
        _USERS.extend(users)
        if not __ifFileExists('available_books.csv'):
            with open('available_books.csv', 'x') as bookfile:
                bookwriter= csv.writer(bookfile, delimiter=',')
                bookwriter.writerows(list(booklist))
        if not __ifFileExists('loaned_books.csv'):
            with open('loaned_books.csv', 'x') as bookfile:
                bookwriter= csv.writer(bookfile, delimiter=',')
                bookwriter.writerow(["title","author","is_loaned","copies","genre","year"])
        if not __ifFileExists('log.txt'):
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
            booklist.writerow([
                book._title,
                book._author,
                __yesNoBool(book.wasLoaned()),
                book._copies,
                str(book._genre),
                book._year
            ])

    def addBook(self, book: Book):
        """
        Adds a book to the library.
        """
        BOOKS.append(book)
        try:
            # add new book to csv
            self.__addBookToCSV(book, 'books.csv')
            self.__log__('book added successfully')
        except OSError:
            self.__log__('book added fail')

    def __removeBookFromCSV(self, book: Book, csvfile: str):
        """
        Internal method to remove a book from the given csvfile path.
        """
        # read csv
        bookfile= __csvAsMatrix(csvfile)
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
        try:
            self.__removeBookFromCSV(book, 'books.csv')
            self.__log__('book removed successfully')
        except OSError:
            self.__log__('book removed fail')

    def updateBookDetails(self, index: int, newBook: Book, csvfile: str):
        """
        Updates the details of the book in the specified index.
        """
        BOOKS[index]= newBook
        # read csv
        bookfile= __csvAsMatrix(csvfile)
        # update relevant row
        newrow= [
                    newBook._title,
                    newBook._author,
                    __boolYesNo(newBook._wasLoaned()),
                    newBook._copies,
                    str(newBook._genre),
                    newBook._year
                ]
        rows= [newrow if i == index else row for i, row in enumerate(bookfile)]
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
        _USERS.append(newuser)
        if not __ifFileExists('users.csv'):
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
        # find book in available
        available= __csvAsMatrix('available_books.csv')
        for i, row in enumerate(available):
            if row[0] == bookname:
                book_to_borrow= row
                index= i
        # can borrow
        while book_to_borrow._copies > 0:
            # update book
            book_to_borrow._copies-=1
            if book_to_borrow._copies == 0:
                book_to_borrow[2]= 'Yes'
            else:
                book_to_borrow[2]= 'No'
            try:
                # update available books
                self.updateBookDetails(index, book_to_borrow, 'available_books.csv')
                # find book in loaned
                loaned= __csvAsMatrix('loaned_books.csv')
                for i, row in enumerate(loaned):
                    if row[0] == bookname:
                        loaned_book= row
                        index= i
                # update loaned books
                if loaned_book:
                    loaned_book[3]-=1
                    self.updateBookDetails(index, loaned_book, 'loaned_books.csv')
                else:
                    self.__addBookToCSV(book_to_borrow, 'loaned_books.csv')
                return
            except OSError:
                break
        self.__log__('book borrowed fail')