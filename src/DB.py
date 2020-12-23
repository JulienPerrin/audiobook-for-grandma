import os
import sqlite3
from datetime import datetime
from os import listdir
from os.path import isfile, join


class DB():
    tableName = "afg.db"
    createFilePath = join(os.path.dirname(__file__), 'sql', 'create.sql')

    def __init__(self):
        try:
            self.connexion = sqlite3.connect('afg.db')
            self.cursor = self.connexion.cursor()

            with open(self.createFilePath) as createFile:
                self.cursor.executescript(createFile.read())
            self.connexion.commit()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def __del__(self):
        if self.connexion:
            self.connexion.close()

    def lastBook(self) -> str:
        self.cursor.execute("SELECT identifier FROM CONTINUE_READING")
        result = self.cursor.fetchone()
        if result is None: 
            return None
        else: 
            return result[0]

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

    def updateBookmark(self, identifier: str, lastLineRead: int):
        if self.getBookmark(identifier) is not None:
            # print("UPDATE BOOKMARK: {} {}".format(identifier, lastLineRead))
            self.cursor.execute(
                "UPDATE BOOKMARK SET line_number=? WHERE identifier = ?", (lastLineRead, identifier))
        else:
            print("INSERT BOOKMARK: {} {}".format(identifier, lastLineRead))
            self.cursor.execute(
                "INSERT INTO BOOKMARK VALUES (?, ?)", (identifier, lastLineRead))
        self.connexion.commit()

    def getBookmark(self, identifier: str) -> int:
        self.cursor.execute(
            "SELECT * FROM BOOKMARK WHERE identifier = ?", (identifier,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[1]
        else:
            return None
