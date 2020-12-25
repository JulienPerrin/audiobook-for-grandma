from os import listdir
from os.path import isfile, join, isdir


class Book():
    identifier: str
    title: str
    genre: list[str]
    creator: str
    downloads: str
    encoding: str
    genre: str
    name: str
    publicdate: str
    publisher: str
    title: str
    volume: str
    pathOfFileToRead: str

    def __init__(self, identifier: str):
        self.identifier = identifier
        self.genre = []

        path = join('out', 'gutenberg', identifier)
        if (isdir(path)):
            files = [f for f in listdir(path) if isfile(join(path, f))]
            print("files in path of file to read", files)
            if files and len(files) > 0:
                self.pathOfFileToRead = join(path, files[0])
