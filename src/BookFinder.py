import os
from os import listdir
from os.path import isfile, join

import requests
from internetarchive import download

from .DB import DB
from .model.Book import Book


class BookFinder():
    language: str
    db: DB

    def __init__(self, db, language='fr'):
        self.language = language
        self.db = db
        if not self.db.isBookListDownloaded():
            self.downloadBookList()

    def downloadBookList(self) -> ():
        # not good :
        # https://archive.org/advancedsearch.php?q=collection%3A%28gutenberg%29+AND+mediatype%3A%28texts%29+AND+language%3A%28fr%29&fl%5B%5D=creator&fl%5B%5D=downloads&fl%5B%5D=format&fl%5B%5D=subject&fl%5B%5D=identifier&fl%5B%5D=name&fl%5B%5D=publicdate&fl%5B%5D=publisher&fl%5B%5D=title&fl%5B%5D=volume&sort%5B%5D=downloads+desc&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&callback=callback&save=yes#raw
        # better use scrapping API :
        END_POINT = "https://archive.org/services/search/v1/scrape"
        QUERY = "q=collection%3A%28gutenberg%29+AND+mediatype%3A%28texts%29+AND+language%3A%28fr%29"
        FIELDS = "fields=creator,downloads,identifier,publicdate,publisher,title,volume,subject"
        URL = "{}?{}&{}".format(END_POINT, QUERY, FIELDS)
        basic_params = {}
        result = requests.get(URL, basic_params)
        while True:
            if result.status_code == 200:
                json = result.json()
                items = json.get('items')
                if items is not None:
                    self.db.addBooks([
                        Book(
                            identifier=item.get('identifier'),
                            title=item.get('title'),
                            creator=item.get('creator'),
                            downloads=item.get('downloads'),
                            publisher=item.get('publisher'),
                            volume=item.get('volume', None),
                            # TODO: add item.get('subject', None),
                        )
                        for item in items
                    ])
                cursor = json.get('cursor')
                if cursor is None:
                    break
                else:
                    params = basic_params.copy()
                    params['cursor'] = cursor
                    result = requests.get(URL, params=params)
            else:
                break

    def findBook(self) -> Book:
        lastBook = self.db.lastBook()
        if lastBook is not None and not self.db.isSkipped(lastBook.identifier) and not self.db.isFinished(lastBook.identifier):
            return lastBook
        else:
            print("Let's find the next book!")
            nextBook = self.db.findNextBook()
            if nextBook is None:
                raise ValueError("No more books to read")
            download(nextBook.identifier, destdir=join('out', 'gutenberg'),
                     verbose=True, checksum=True, glob_pattern='*txt', ignore_existing=True)
            nextBook.updatePathOfFileToRead()
            print('Book downloaded:', nextBook)
            return nextBook
