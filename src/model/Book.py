from os import listdir
from os.path import isfile, join

from .Bookmark import Bookmark

class Book():
    gutenbergIdentifier: str
    title: str
    bookmark: Bookmark
    genre: list[str]
    creator: str
    downloads: str
    format: str
    genre: str
    identifier: str
    name: str
    publicdate: str
    publisher: str
    title: str
    volume: str
    pathOfFileToRead: str

    def __init__(self, gutenbergIdentifier: str):
        self.gutenbergIdentifier = gutenbergIdentifier

        path = join('out', 'gutenberg', gutenbergIdentifier)
        files = [f for f in listdir(path) if isfile(join(path, f))]
        print("files in path of file to read", files)
        if files and len(files) > 0:
            self.pathOfFileToRead = join(path, files[0])
        else:
            raise ValueError("the file for the book does not exists")

        self.bookmark = Bookmark()
