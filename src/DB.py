import os
import sqlite3
from datetime import datetime
from os import listdir
from os.path import isfile, join

from .model.Book import Book


class DB():
    tableName = "afg.db"
    createFilePath = join(os.path.dirname(__file__), 'sql', 'create.sql')
    dropFilePath = join(os.path.dirname(__file__), 'sql', 'drop.sql')
    testFilePath = join(os.path.dirname(__file__), 'sql', 'insert_test.sql')
    findNextBookFilePath = join(os.path.dirname(
        __file__), 'sql', 'find_next_book.sql')

    def __init__(self):
        try:
            self.connexion = sqlite3.connect('afg.db')
            self.cursor = self.connexion.cursor()

            with open(self.createFilePath) as createFile:
                self.cursor.executescript(createFile.read())
            self.connexion.commit()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def test(self):
        with open(self.dropFilePath) as dropFile:
            self.cursor.executescript(dropFile.read())
        with open(self.createFilePath) as createFile:
            self.cursor.executescript(createFile.read())
        with open(self.testFilePath) as testFile:
            self.cursor.executescript(testFile.read())
        self.connexion.commit()

    def __del__(self):
        if self.connexion:
            self.connexion.close()

    def addBooks(self, books: list):
        self.cursor.executemany(
            "DELETE FROM BOOK WHERE identifier = ?",
            [(book.identifier,) for book in books]
        )
        self.cursor.executemany(
            "DELETE FROM SUBJECT WHERE identifier = ?",
            [(book.identifier,) for book in books]
        )
        self.cursor.executemany("""
            INSERT INTO BOOK 
            (IDENTIFIER,TITLE,CREATOR,DOWNLOADS,PUBLISHER,VOLUME,ENCODING,DOWNLOADED)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                                [
                                    (
                                        str(book.identifier),
                                        str(book.title),
                                        str(book.creator),
                                        int(book.downloads),
                                        str(book.publisher),
                                        str(book.volume),
                                        None,
                                        bool(book.downloaded),
                                    ) for book in books
                                ]
                                )
        self.cursor.executemany("""
            INSERT INTO SUBJECT 
            (IDENTIFIER,NAME)
            SELECT ?, ? WHERE NOT EXISTS(SELECT 1 FROM SUBJECT s WHERE s.IDENTIFIER = ? AND s.NAME = ?)
            """,
                                [
                                    (
                                        str(book.identifier),
                                        str(subject),
                                        str(book.identifier),
                                        str(subject),
                                    ) for book in books for subject in book.subjects
                                ]
                                )
        self.connexion.commit()

    def isBookListDownloaded(self):
        self.cursor.execute("SELECT COUNT(*) FROM BOOK")
        count = self.cursor.fetchone()
        return count is not None and count[0] > 100

    def updateEncoding(self, identifier: str, encoding: str) -> ():
        self.cursor.execute(
            "UPDATE BOOK SET ENCODING = ? WHERE IDENTIFIER = ?", (encoding, identifier))
        self.connexion.commit()

    def findNextBook(self) -> Book:
        with open(self.findNextBookFilePath) as findNextBookFile:
            self.cursor.execute(findNextBookFile.read())
        return self.fetchBook()

    def lastBook(self) -> Book:
        self.cursor.execute("""
        SELECT book.IDENTIFIER, book.TITLE, book.CREATOR, book.DOWNLOADS, book.PUBLISHER, book.VOLUME, book.ENCODING, book.DOWNLOADED
        FROM CONTINUE_READING cr 
        JOIN BOOK book ON BOOK.IDENTIFIER = cr.IDENTIFIER
        """)
        return self.fetchBook()

    def listAllBooks(self) -> list:
        self.cursor.execute("""
        SELECT book.IDENTIFIER, book.TITLE, book.CREATOR, book.DOWNLOADS, book.PUBLISHER, book.VOLUME, book.ENCODING, book.DOWNLOADED
        FROM BOOK book
        """)
        return [Book(
                identifier=result[0],
                title=result[1],
                creator=result[2],
                downloads=result[3],
                publisher=result[4],
                volume=result[5],
                encoding=result[6],
                downloaded=result[7],
                ) for result in self.cursor.fetchall()]

    def fetchBook(self) -> Book:
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return Book(
                identifier=result[0],
                title=result[1],
                creator=result[2],
                downloads=result[3],
                publisher=result[4],
                volume=result[5],
                encoding=result[6],
                downloaded=result[7],
            )

    def markDownloaded(self, book: Book) -> ():
        self.cursor.execute(
            "UPDATE BOOK SET DOWNLOADED = 1 WHERE IDENTIFIER = ?", (book.identifier,))
        self.connexion.commit()

    def updateContinueReading(self, continueReading: bool, identifier):
        if not identifier or identifier is None:
            raise ValueError('identifier is not defined:', identifier)
        self.cursor.execute("DELETE FROM CONTINUE_READING")
        data_tuple = (continueReading, datetime.now(), identifier)
        self.cursor.execute(
            "INSERT INTO CONTINUE_READING VALUES (?, ?, ?)", data_tuple)
        self.connexion.commit()

    def isContinueReading(self) -> bool:
        self.cursor.execute("SELECT * FROM CONTINUE_READING")
        return self.cursor.fetchone()[0]

    def updateBookmark(self, identifier: str, lastLineRead: int, numberOfLines: int = None):
        if self.getBookmark(identifier) is not None:
            # print("UPDATE BOOKMARK: {} {}".format(identifier, lastLineRead))
            self.cursor.execute(
                "UPDATE BOOKMARK SET line_number=? WHERE identifier = ?", (lastLineRead, identifier))
        else:
            print("INSERT INTO BOOKMARK VALUES ({}, {}, {}, {}, {})".format(
                identifier, lastLineRead, numberOfLines, False, False))
            self.cursor.execute(
                "INSERT INTO BOOKMARK VALUES (?, ?, ?, ?, ?)", (identifier, lastLineRead, numberOfLines, False, False))
        self.connexion.commit()

    def getBookmark(self, identifier: str) -> int:
        self.cursor.execute(
            "SELECT * FROM BOOKMARK WHERE identifier = ?", (identifier,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[1]
        else:
            return None

    def skip(self) -> ():
        self.cursor.execute(
            "UPDATE BOOKMARK SET SKIPPED=1 WHERE identifier = ?", (self.lastBook().identifier,))
        self.connexion.commit()

    def isSkipped(self, identifier: str) -> bool:
        self.cursor.execute(
            "SELECT SKIPPED FROM BOOKMARK WHERE identifier = ?", (identifier,))
        result = self.cursor.fetchone()
        return result is not None and result[0]

    def markFinished(self) -> ():
        self.cursor.execute(
            "UPDATE BOOKMARK SET FINISHED=1 WHERE identifier = ?", (self.lastBook().identifier,))
        self.connexion.commit()

    def isFinished(self, identifier: str) -> bool:
        self.cursor.execute(
            "SELECT FINISHED FROM BOOKMARK WHERE identifier = ?", (identifier,))
        result = self.cursor.fetchone()
        return result is not None and result[0]
