import abc
from datetime import datetime

from .DB import DB
from .model.Book import Book


class BookFinder():
    language: str
    db: DB
    publisher: str
    

    def __init__(self, db, publisher, language='fr'):
        self.language = language
        self.db = db
        self.publisher = publisher
        if not self.db.isBookListDownloaded():
            self.downloadBookList()

    @abc.abstractmethod
    def downloadBookList(self) -> None:
        raise NotImplementedError(
            'Need to define method to use this base class.')

    def findBook(self) -> Book:
        lastBook = self.db.lastBook()
        if lastBook is not None and not self.db.isSkipped(lastBook.identifier) and not self.db.isFinished(lastBook.identifier):
            return lastBook
        else:
            print(datetime.now(), "Let's find the next book!")
            nextBook = self.db.findNextBook()
            if nextBook is None:
                raise ValueError("No more books to read")
            print(datetime.now(), "Book found:", nextBook)
            if not nextBook.downloaded:
                self.downloadBook(nextBook)
            return nextBook

    @abc.abstractmethod
    def downloadBook(self, book: Book) -> None:
        raise NotImplementedError(
            'Need to define method to use this base class.')
