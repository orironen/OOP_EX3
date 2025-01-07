from copy import deepcopy
import csv
from book import Book, Genre

def yesNoBool(string: str) -> bool:
    """
    Returns True if the string is 'Yes', False otherwise.
    """
    if string == 'Yes':
        return True
    return False

def boolYesNo(boolean: bool) -> str:
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
        with open('books.csv', 'r', newline='') as books:
            booklist = csv.reader(books, delimiter=',')
            self.books = []
            for row in booklist:
                self.books.append(Book(
                    row[0], 
                    row[1], 
                    yesNoBool(row[2]), 
                    int(row[3]), 
                    Genre.parseGenre(row[4]), 
                    int(row[5])
                ))
        self.users= deepcopy(users)

    def addBook(self, book: Book):
        """
        Adds a book to the library.
        """
        self.books.append(book)
        with open('books.csv', 'a', newline='') as books:
            booklist = csv.writer(books, delimiter=',')
            booklist.writerow([
                book._title,
                book._author,
                yesNoBool(book.wasLoaned()),
                book._copies,
                str(book._genre),
                book._year
            ])

    def removeBook(self, book: Book):
        """
        Removes a book from the library.
        """
        self.books.remove(book)
        # read csv
        with open('books.csv', 'r', newline='') as books:
            bookreader = csv.reader(books, delimiter=',')
            bookfile = list(bookreader)
        # remove relevant row
        for row in bookfile:
            if row[0] == book._title:
                bookreader.remove(row)
        # rejoin csv
        output= ','.join(row for row in bookfile)
        with open('books.csv', 'w', newline='') as books:
            books.write(output)


    def updateBookDetails(self, index: int, newBook: Book):
        """
        Updates the details of a book.
        """
        self.books[index]= newBook
        # read csv
        with open('books.csv', 'r', newline='') as books:
            bookreader = csv.reader(books, delimiter=',')
            bookfile = list(bookreader)
        # update relevant row
        for i in len(bookfile):
            if i == index:
                bookfile[index]= [
                    newBook._title,
                    newBook._author,
                    boolYesNo(newBook.wasLoaned()),
                    newBook._copies,
                    str(newBook._genre),
                    newBook._year
                ]
        # rejoin file
        output= ','.join(row for row in bookfile)
        # write to csv
        with open('books.csv', 'w', newline='') as books:
            books.write(output)