from copy import deepcopy
import csv
import random
import string
import hashlib
from abc import ABC, abstractmethod
from Users.user import User
from database.book import Book, BookFactory
import database.strategies as strats
from database.iterators import UserIterator

BOOKS: list[Book] = []
AVAILABLE_BOOKS: list[Book] = []
LOANED_BOOKS: list[Book] = []
USERS: list[User] = []

def _csvToBook(file: str) -> list[Book]:
    """
    Returns a list of Book objects from the csv.
    """
    output: list[Book]= []
    with open(file, 'r', newline='') as bookfile:
        booklist = csv.reader(bookfile, delimiter=',')
        for i, row in enumerate(booklist):
            if i != 0:
                output.append(BookFactory.create_book_from_row(row))
    return output

def _csvAsMatrix(file: str) -> list[list[str]]:
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
        global BOOKS, AVAILABLE_BOOKS, LOANED_BOOKS, USERS
        # get books from csv
        BOOKS= _csvToBook('books.csv')
        # copy into available books
        if not _ifFileExists('available_books.csv'):
            AVAILABLE_BOOKS.extend(book for book in BOOKS if not book.loaned)
            with open('available_books.csv', 'x', newline='') as bookfile:
                writer= csv.writer(bookfile, delimiter=',')
                writer.writerow(["title","author","is_loaned","copies","genre","year"])
                writer.writerows(book.toList() for book in AVAILABLE_BOOKS)
        else:
            AVAILABLE_BOOKS= _csvToBook('available_books.csv')
        if not _ifFileExists('loaned_books.csv'):
            LOANED_BOOKS.extend(book for book in BOOKS if book.loaned)
            with open('loaned_books.csv', 'x', newline='') as bookfile:
                writer= csv.writer(bookfile, delimiter=',')
                writer.writerow(["title","author","is_loaned","copies","genre","year"])
                writer.writerows(book.toList() for book in LOANED_BOOKS)
        else:
            LOANED_BOOKS= _csvToBook('loaned_books.csv')
        # get user data
        if not _ifFileExists('users.csv'):
            with open('users.csv', 'x', newline='') as userfile:
                userwriter= csv.writer(userfile, delimiter=',')
                userwriter.writerow(["name","password","salt"])
        else:
            with open('users.csv', 'r') as userfile:
                userreader= csv.reader(userfile, delimiter=',')
                for i, row in enumerate(userreader):
                    if i != 0:
                        USERS.append(User.parseUser(row))
        # create log.txt
        if not _ifFileExists('log.txt'):
            with open('log.txt', 'x') as log:
                log.write('')

    def __log__(self, action: str):
        """
        Logs an action into the log file.
        """
        with open('log.txt', 'a') as log:
            log.write(f'{action}\n')

    def notify(self, message: str):
        """
        Notify the inputted message to all observers.
        """
        for user in USERS:
            user.update(message)

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
            self.notify(f'The book {book.title} has been added.')
        except OSError:
            self.__log__('book added fail')
            raise OSError

    def __removeBookFromCSV(self, book: Book, csvfile: str):
        """
        Internal method to remove a book from the given csvfile path.
        """
        # read csv
        bookfile= _csvAsMatrix(csvfile)
        # remove relevant row
        rows= [row for row in bookfile if row[0] == book.title]
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
            self.notify(f'The book {book.title} has been removed.')
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
        rows= [newBook.toList() if oldBook.title == row[0] else row for row in bookfile]
        # write to csv
        with open(csvfile, 'w', newline='') as books:
            bookwriter= csv.writer(books)
            bookwriter.writerows(rows)

    def registerUser(self, name: str, password: str) -> bool:
        """
        Register a user to the library. Returns True if registered, False otherwise.
        """
        # generate random salt
        salt= ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        pword= hashlib.sha256((password+salt).encode()).hexdigest()
        # create user
        newuser= User(name, pword, salt)
        USERS.append(newuser)
        try:
            with open('users.csv', 'a', newline='') as userfile:
                userwriter= csv.writer(userfile, delimiter=',')
                userwriter.writerow([name, pword, salt])
            self.__log__("registered successfully")
            self.notify(message=f"{newuser.name}'s account has been created successfully.")
            return True
        except OSError:
            self.__log__("registered fail")
            return False

    def logInUser(self, username: str, password: str) -> bool:
        """
        Returns True if the password matches the username.
        """
        current= None
        userIter= UserIterator()
        while userIter.hasNext():
            user= userIter.next()
            if user.name == username:
                current= user
        if current and current.passwordMatch(password):
            self.__log__('logged in successfully')
            self.notify(message=f"{current.name} has logged in.")
            return True
        else:
            self.__log__('logged in fail')
            return False
        
    def logOutUser(self):
        """
        Method that records that the user was logged out.
        """
        self.__log__('logged out successfully')
        
    def borrowBook(self, loaner: str, bookname: str):
        """
        Borrows a book from the library in the name of the
        mentioned user.
        """
        try:
            # find book in available
            book_to_borrow: Book
            try:
                booksearch= strats.AvailableDecorator(strats.SearchByTitle())
                book_to_borrow= deepcopy(booksearch.search(bookname)[0])
            except IndexError:
                # add to waiting list
                booksearch= strats.SearchByTitle()
                book_to_borrow= deepcopy(booksearch.execute_search(bookname)[0])
                book_to_borrow.addToWaitingList(loaner)
                self.notify(f"{loaner} has been added to the waiting list for '{bookname}'.")
                raise OSError
            oldbook= deepcopy(book_to_borrow)
            # update book
            book_to_borrow.copies-=1
            book_to_borrow.loaned= True
            # update available books
            self.updateBookDetails(oldbook, book_to_borrow, 'available_books.csv')
            # find book in loaned
            try:
                booksearch= strats.LoanedDecorator(strats.SearchByTitle())
                loaned_book= deepcopy(booksearch.search(bookname)[0])
                # update loaned books
                oldbook= deepcopy(loaned_book)
                loaned_book.copies+=1
                self.updateBookDetails(oldbook, loaned_book, 'loaned_books.csv')
            except IndexError:
                book_to_borrow.copies= 1
                self.__addBookToCSV(book_to_borrow, 'loaned_books.csv')
            book_to_borrow.removeFromWaitingList(loaner)
            self.notify(message=f"The book '{book_to_borrow.title}' was borrowed by {loaner}.")
        except OSError:
            self.__log__('book borrowed fail')

    def returnBook(self, loaner: str, bookname: str):
        """
        Borrows a book from the library in the name of the
        mentioned user.
        """
        try:
            book_to_return: Book
            # find book in available
            booksearch= strats.AvailableDecorator(strats.SearchByTitle())
            book_to_return= deepcopy(booksearch.search(bookname)[0])
            oldbook= deepcopy(book_to_return)
            # update book
            book_to_return.copies-=1
            book_to_return.loaned= False
            # update available books
            self.updateBookDetails(oldbook, book_to_return, 'loaned_books.csv')
            # find book in loaned
            try:
                booksearch= strats.LoanedDecorator(strats.SearchByTitle())
                book_to_return= deepcopy(booksearch.search(bookname)[0])
                # update loaned books
                oldbook= deepcopy(book_to_return)
                book_to_return.copies+=1
                self.updateBookDetails(oldbook, book_to_return, 'available_books.csv')
            except IndexError:
                book_to_return.copies= 1
                # notify to waiting list
                self.notify(message= f"The book {book_to_return.title} has returned.")
                self.__addBookToCSV(book_to_return, 'available_books.csv')
            book_to_return.borrowed-=1
            if loaner in book_to_return.getWaitingList():
                book_to_return.removeFromWaitingList(loaner)
            self.__log__('book returned successfully')
            self.notify(message=f"The book '{book_to_return.title}' was returned by {loaner}.")
        except OSError:
            self.__log__('book borrowed fail')

    def viewBooklist(self, category: str, books: list[Book]= None):
        """
        Returns a list of Book objects in the library with various effects.
        """
        if not books:
            books= BOOKS
        
        if category == "all":
            bookview= strats.ViewBooklist(books)
            self.__log__('Displayed all books successfully')
        elif category == "available":
            bookview= strats.ViewBooklist([book for book in books if book in AVAILABLE_BOOKS])
            self.__log__('Displayed available books successfully')
        elif category == "loaned":
            bookview= strats.ViewBooklist([book for book in books if book in LOANED_BOOKS])
            self.__log__('Displayed borrowed books successfully')
        elif category == "popular":
            bookview= strats.PopularDecorator(strats.ViewBooklist(books))
            self.__log__('Displayed popular books successfully')
        return bookview.view()
    
    def sortByTitle(self, books: list[Book]):
        """
        View books by title.
        """
        bookview= strats.AlphabeticalDecorator(strats.ViewBooklist(books))
        return bookview.view()
    
    def sortByGenre(self, books: list[Book]):
        """
        View books by genre.
        """
        self.__log__('Displayed book by category successfully')
        bookview= strats.GenreDecorator(strats.ViewBooklist(books))
        return bookview.view()
    
    def searchBooklist(self, query: str, searchby: str):
        """
        Searches the booklist based on the query and the value key.
        """
        if searchby == "Title":
            self.__log__(f'Search book "{query}" by name completed successfully')
            comp= strats.SearchByTitle(BOOKS)
        elif searchby == "Author":
            self.__log__(f'Search book "{query}" by author completed successfully')
            comp= strats.SearchByAuthor(BOOKS)
        elif searchby == "Genre":
            self.__log__(f'Search book "{query}" by category completed successfully')
            comp= strats.SearchByGenre(BOOKS)
        elif searchby == "Year":
            self.__log__(f'Search book "{query}" by year completed successfully')
            comp= strats.SearchByYear(BOOKS)
        return comp.search(query)