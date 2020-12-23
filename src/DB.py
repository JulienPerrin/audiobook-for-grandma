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
            self.updateContinueReading(True)
            self.connexion.commit()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def __del__(self):
        if self.connexion:
            self.connexion.close()

    def updateContinueReading(self, continueReading: bool):
        self.cursor.execute("DELETE FROM CONTINUE_READING")
        data_tuple = (continueReading, datetime.now())
        self.cursor.execute("INSERT INTO CONTINUE_READING VALUES (?, ?)", data_tuple)
        self.connexion.commit()

    def isContinueReading(self) -> bool:
        self.cursor.execute("SELECT * FROM CONTINUE_READING")
        return self.cursor.fetchone()[0]

