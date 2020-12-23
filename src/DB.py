import sqlite3


class DB():
    createFilePath = "./sql/create.sql"

    def __init(self, connection):
        self.connection = sqlite3.connect('afg.db')
        self.cursor = connection.cursor()

        with open(self.createFilePath) as createFile:
            self.cursor.executescript(createFile.read())
        self.connection.commit()
