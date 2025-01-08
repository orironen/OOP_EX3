import hashlib

from database.book import Book

class User:
    """
    Represents a User. Includes its username, password, and the
    books they borrowed.
    """
    def __init__(self, name: str, password: str, salt: str):
        self.name = name
        self.__salt = salt
        self.__password = password

    def passwordMatch(self, entered: str) -> bool:
        """
        Check if the given phrase matches the login password.
        """
        return hashlib.sha256((entered+self.__salt).encode()) == self.__password
    
    
