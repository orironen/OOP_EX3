import hashlib

from database.book import Book

class User:
    """
    Represents a User. Includes its username, password, and the
    books they borrowed. Also implements the Observer design pattern.
    """
    def __init__(self, name: str, password: str, salt: str):
        self.name = name
        self.__salt = salt
        self.__password = password
        self.__messages: list[str]= []

    def passwordMatch(self, entered: str) -> bool:
        """
        Check if the given phrase matches the login password.
        """
        return hashlib.sha256((entered+self.__salt).encode()) == self.__password
    
    def update(self, message: str):
        self.__messages.append(message)

    def getNotifications(self):
        return self.__messages