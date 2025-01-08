from Users.user import User
from database import library
from database.book import Book

class __Iterator:
    """
    Base class for the Iterator design pattern.
    """
    def __init__(self, l: list):
        self.__i= 0
        self.__l= l

    def hasNext(self) -> bool:
        """
        Returns True if the Iterator didn't reach the final item, False otherwise.
        """
        return self.__i < len(self.__l)
    
    def next(self):
        """
        Returns the next iterated item.
        """
        try:
            output= self.__l[self.__i]
            self.__i+=1
            return output
        except IndexError:
            raise IndexError('No more items to iterate on.')
        
class UserIterator(__Iterator):
    """
    Iterator for library users.
    """
    def __init__(self):
        super().__init__(library.USERS)

    def next(self) -> User:
        return super().next()

class BookIterator(__Iterator):
    """
    Iterator for library books.
    """
    def __init__(self, books: list[Book]):
        super().__init__(books)

    def next(self) -> Book:
        return super().next()