import linecache
import logging.config
import os
from os import listdir
from os.path import isfile, join

import wget
import yaml
from internetarchive import download, search_items

from .model.Book import Book
from .DB import DB


class BookFinder():
    language: str
    db: DB

    def __init__(self, db, language='fr'):
        self.language = language
        self.db = db

    def findBook(self) -> Book:
        # https://archive.org/advancedsearch.php?q=collection%3A%28gutenberg%29+AND+mediatype%3A%28texts%29+AND+language%3A%28fr%29&fl%5B%5D=creator&fl%5B%5D=downloads&fl%5B%5D=format&fl%5B%5D=genre&fl%5B%5D=identifier&fl%5B%5D=name&fl%5B%5D=publicdate&fl%5B%5D=publisher&fl%5B%5D=title&fl%5B%5D=volume&sort%5B%5D=downloads+desc&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&callback=callback&save=yes#raw
        for item in search_items(query='collection:(gutenberg) AND mediatype:(texts) AND language:({})'.format(self.language)):
            skipped = self.db.isSkipped(item['identifier'])
            if (skipped):
                continue
            print('item: {}, skipped: {}'.format(str(item), str(skipped)))
            download(item['identifier'], destdir=join('out', 'gutenberg'),
                     verbose=True, checksum=True, glob_pattern='*txt', ignore_existing=True)
            return Book(item['identifier'])
