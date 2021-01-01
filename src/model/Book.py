from os import listdir
from os.path import isfile, join, isdir


class Book():
    identifier: str
    title: str
    creator: str
    downloads: str
    publisher: str
    volume: str
    pathOfFileToRead: str
    encoding: str
    downloaded: bool
    subjects: list

    def __init__(self, identifier: str, title: str, creator: str, downloads: str, publisher: str, 
            volume: str, downloaded: bool, subjects: list = [], encoding: str = None):
        self.identifier = identifier
        self.title = title
        self.creator = creator
        self.downloads = downloads
        self.publisher = publisher
        self.volume = volume
        self.encoding = encoding
        self.subjects = subjects
        self.downloaded = downloaded
        self.updatePathOfFileToRead()
        
    def updatePathOfFileToRead(self):
        path = join('out', 'gutenberg', self.identifier)
        if (isdir(path)):
            files = [f for f in listdir(path) if isfile(join(path, f))]
            if files and len(files) > 0:
                self.pathOfFileToRead = join(path, files[0])

    def __str__(self):
        return "Book: [title: {} / identifier: {}]".format(self.title, self.identifier)

    def __getitem__(self, item):
         return getattr(self, item)
