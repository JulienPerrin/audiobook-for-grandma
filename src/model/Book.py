from os import listdir
from os.path import isfile, join


class Book():
    identifier: str
    title: str
    genre: list[str]
    creator: str
    downloads: str
    format: str
    genre: str
    name: str
    publicdate: str
    publisher: str
    title: str
    volume: str
    pathOfFileToRead: str

    def __init__(self, identifier: str):
        self.identifier = identifier

        path = join('out', 'gutenberg', identifier)
        files = [f for f in listdir(path) if isfile(join(path, f))]
        print("files in path of file to read", files)
        if files and len(files) > 0:
            self.pathOfFileToRead = join(path, files[0])
        else:
            raise ValueError("the file for the book does not exists")
