import csv
from database.book import Book

def yesNoBool(string):
    if string == 'Yes':
        return True
    return False

def read_from_csv() -> Book:
    """
    Reads a file called 'books.csv' and returns a list of Book objects.
    """
    with open('books.csv', 'r', newline='') as books:
        booklist = csv.reader(books, delimiter=',')
        books = []
        for row in booklist:
            books.append(Book(row[0], row[1], yesNoBool(row[2]), int(row[3]), row[4], int(row[5])))
    return books

read_from_csv()