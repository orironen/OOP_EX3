from copy import deepcopy
import csv
import random
import string
import hashlib
from Users.user import User
from book import Book, Genre

def csvAsMatrix(file: str) -> list:
    """
    Returns a matrix representing the rows of the csv file.
    """
    with open(file, 'r', newline='') as f:
        return list(csv.reader(f, delimiter=','))

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
    def __init__(self, users):
        # get books from csv
        with open('books.csv', 'r', newline='') as books:
            booklist = csv.reader(books, delimiter=',')
            self.books = []
            for row in booklist:
                self.books.append(Book(
                    row[0], 
                    row[1], 
                    __yesNoBool(row[2]), 
                    int(row[3]), 
                    Genre.parseGenre(row[4]), 
                    int(row[5])
                ))
        self.users= deepcopy(users)
        with open('log.txt', 'w') as log:
            log.write('')

    def __log__(self, action: str):
        """
        Logs an action into the log file.
        """
        with open('log.txt', 'a') as log:
            log.write(f'{action}\n')

    def addBook(self, book: Book):
        """
        Adds a book to the library.
        """
        self.books.append(book)
        try:
            # add new book to csv
            with open('books.csv', 'a', newline='') as books:
                booklist = csv.writer(books, delimiter=',')
                booklist.writerow([
                    book._title,
                    book._author,
                    __yesNoBool(book.wasLoaned()),
                    book._copies,
                    str(book._genre),
                    book._year
                ])
            self.__log__('book added successfully')
        except OSError:
            self.__log__('book added fail')

    def removeBook(self, book: Book):
        """
        Removes a book from the library.
        """
        self.books.remove(book)
        try:
            # read csv
            bookfile= csvAsMatrix('books.csv')
            # remove relevant row
            rows= [row for row in bookfile if row[0] == book._title]
            # write to csv
            with open('books.csv', 'w', newline='') as books:
                bookwriter= csv.writer(books)
                bookwriter.writerows(rows)
            self.__log__('book removed successfully')
        except OSError:
            self.__log__('book removed fail')

    def updateBookDetails(self, index: int, newBook: Book):
        """
        Updates the details of the book in the specied index.
        """
        self.books[index]= newBook
        # read csv
        bookfile= csvAsMatrix('books.csv')
        # update relevant row
        newrow= [
                    newBook._title,
                    newBook._author,
                    __boolYesNo(newBook.wasLoaned()),
                    newBook._copies,
                    str(newBook._genre),
                    newBook._year
                ]
        rows= [newrow if i == index else row for i, row in enumerate(bookfile)]
        # write to csv
        with open('books.csv', 'w', newline='') as books:
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
        self.users.append(newuser)
        try:
            open('users.csv', 'r')
        except OSError:
            with open('users.csv', 'x') as userfile:
                userwriter= csv.writer(userfile, delimiter=',')
                userwriter.writerow(["name","password","salt","borrowed"])
        try:
            with open('user.csv', 'a') as userfile:
                userwriter= csv.writer(userfile, delimiter=',')
                userwriter.writerow([name, password, salt, []])
            self.__log__("registered successfully")
            return newuser
        except OSError:
            self.__log__("registered fail")

    