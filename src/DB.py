import os
import sqlite3
from datetime import datetime
from os import listdir
from os.path import isfile, join

from .model.Book import Book


class DB():
    tableName = "afg.db"
    createFilePath = join(os.path.dirname(__file__), 'sql', 'create.sql')
    testFilePath = join(os.path.dirname(__file__), 'sql', 'insert_test.sql')

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
        with open(self.testFilePath) as testFile:
            self.cursor.executescript(testFile.read())
        self.connexion.commit()

    def __del__(self):
        if self.connexion:
            self.connexion.close()

    def addBooks(self, books: list[Book]):
        self.cursor.executemany(
            "DELETE FROM BOOK WHERE identifier = ?",
            [(book.identifier,) for book in books]
        )
        self.cursor.executemany("""
            INSERT INTO BOOK 
            (IDENTIFIER,FORMAT,NAME,TITLE,CREATOR,GENRE,DOWNLOADS,PUBLICDATE,PUBLISHER,VOLUME)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                            [
                                (
                                    book.identifier,
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    '',
                                    ''
                                ) for book in books
                            ]
                            )
        self.connexion.commit()

    def isBookListDownloaded(self):
        self.cursor.execute("SELECT 1 FROM BOOK")
        return self.cursor.fetchone() is not None

    def findNextBook(self) -> str:
        self.cursor.execute("""
        SELECT book.IDENTIFIER FROM BOOK book
        LEFT JOIN BOOKMARK bookmark ON bookmark.IDENTIFIER = book.IDENTIFIER
        WHERE (bookmark.SKIPPED IS NULL OR bookmark.SKIPPED = 0)
        AND (bookmark.FINISHED IS NULL OR bookmark.FINISHED = 0)
        ORDER BY book.DOWNLOADS DESC, book.IDENTIFIER ASC
        """)
        result = self.cursor.fetchone()[0]
        if result is None:
            raise ValueError('No new books to read')
        else:
            return result

    def lastBook(self) -> Book:
        self.cursor.execute("SELECT identifier FROM CONTINUE_READING")
        result = self.cursor.fetchone()
        if result is None:
            return None
        else:
            return Book(result[0])

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

    def updateBookmark(self, identifier: str, lastLineRead: int, numberOfLines: int):
        if self.getBookmark(identifier) is not None:
            # print("UPDATE BOOKMARK: {} {}".format(identifier, lastLineRead))
            self.cursor.execute(
                "UPDATE BOOKMARK SET line_number=? WHERE identifier = ?", (lastLineRead, identifier))
        else:
            print("INSERT BOOKMARK: {} {} {}".format(
                identifier, lastLineRead, False))
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

