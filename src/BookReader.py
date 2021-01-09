import os
from os.path import join

import chardet
import pyttsx3
from chardet.universaldetector import UniversalDetector
from pyttsx3 import engine
from pyttsx3.engine import Engine
from yaml import __version__

from .DB import DB
from .model.Book import Book


class BookReader():
    book: Book
    textToRead: str
    engine: Engine
    db: DB

    def __init__(self, db, defaultRate: int, defaultVolume: float, voice: str, languageTest=''):
        self.textToRead = ''
        self.db = db
        if defaultVolume:
            self.db.setVolume(defaultVolume)
        if defaultRate:
            self.db.setRate(defaultRate)
        self.engine = pyttsx3.init()
        self.engine.setProperty('volume', self.db.getVolume())
        self.engine.setProperty('rate', self.db.getRate())
        voices = [(v.name, v.id) for v in self.engine.getProperty('voices')]
        print("engine voices", voices)
        self.engine.setProperty('voice', voice)
        if languageTest:
            self.engine.say(languageTest)

    def read(self) -> None:
        self.engine.say(self.textToRead)
        self.engine.runAndWait()
        self.textToRead = ''

    def readBook(self, book: Book) -> None:
        self.book = book
        self.textToRead = ''
        # print("path to file to read: ", self.book.pathOfFileToRead)

        if not hasattr(self.book, 'pathOfFileToRead'):
            raise ValueError("Book has not been downloaded")
        self.detectFileEncoding()

        self.db.updateContinueReading(True, self.book.identifier)
        lineNumber = self.db.getBookmark(self.book.identifier)
        if lineNumber is None:
            lineNumber = 0
        if lineNumber == 0:
            self.db.updateBookmark(identifier=self.book.identifier,
                                   lastLineRead=lineNumber, numberOfLines=self.countFileLines())
        with open(self.book.pathOfFileToRead, encoding=self.book.encoding) as bookFile:
            # if we have not already started reading the book, and if the gutenberg intro is at the beginning of the file, then remove it
            if lineNumber == 0 and self.hasGutenbergIntro():
                self.skipGutenbergIntro(bookFile)
            # skip lines until we reach a bit before bookmark
            else:
                for _ in range(0, lineNumber-5):
                    bookFile.readline()
                lineNumber = max(0, lineNumber-4)
            # read the book
            while self.db.isContinueReading() and not self.db.isSkipped(self.book.identifier) and not self.db.isFinished(self.book.identifier):
                self.readBookLine(lineNumber, bookFile.readline())
                self.engine.setProperty('volume', self.db.getVolume())
                self.engine.setProperty('rate', self.db.getRate())
            # read the last sentence if it does not end with a point
            if (self.db.isFinished(self.book.identifier)):
                self.read()
            print('\n')

    def readBookLine(self, lineNumber, fullLine):
        if not fullLine:
            self.db.markFinished()
        line = fullLine.strip() + ' '
        lineNumber += 1
        # print("line {}: {}".format(lineNumber, line))
        if not line.strip():
            return
        sentenceChunks = line.split('.')
        sentenceNumber = -1
        for sentenceChunk in sentenceChunks:
            sentenceNumber += 1
            textStripped = sentenceChunk.strip()
            if not textStripped:
                continue
            if sentenceNumber == 0 and len(sentenceChunks) > 1:
                # the begining of the sentence is on the previous line, the end is on this line
                self.textToRead += '{}. '.format(textStripped)
                print("finished sentence: {}".format(self.textToRead))
                self.db.updateBookmark(
                    identifier=self.book.identifier, lastLineRead=lineNumber)
                self.read()
            elif sentenceNumber == 0:
                # the begining of the sentence is on the previous line
                self.textToRead += '{} '.format(textStripped)
                # print("updated sentence: {}".format(self.textToRead))
            elif sentenceNumber < len(sentenceChunks)-1:
                # the entire sentence is on this line
                self.textToRead = '{}. '.format(textStripped)
                print("sentence: {}".format(self.textToRead))
                self.read()
            else:
                # the end of the sentence is on the next line
                self.textToRead = '{} '.format(textStripped)
                # print("beginned sentence: {}".format(self.textToRead))

    def detectFileEncoding(self) -> None:
        if not hasattr(self.book, 'encoding') or self.book.encoding is None:
            detector = UniversalDetector()
            with open(self.book.pathOfFileToRead, 'rb') as bookFile:
                for line in bookFile:
                    detector.feed(line)
                    if not line:
                        break
                    if detector.done:
                        break
            detector.close()
            encoding = detector.result['encoding']
            print("encoding detected for book {} : {}".format(self.book, encoding))
            self.db.updateEncoding(self.book.identifier, encoding)
            self.book.encoding = encoding

    def countFileLines(self) -> int:
        with open(self.book.pathOfFileToRead, encoding=self.book.encoding) as bookFileWithLinesToCount:
            return sum([1 for _ in bookFileWithLinesToCount])

    def hasGutenbergIntro(self):
        hasGutenbergIntro = False
        with open(self.book.pathOfFileToRead, encoding=self.book.encoding) as bookFile:
            uselessLineIndex = 0
            while uselessLineIndex < 500:
                uselessLine = bookFile.readline()
                uselessLineIndex += 1
                if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                    hasGutenbergIntro = True
                    break
        return hasGutenbergIntro

    def skipGutenbergIntro(self, bookFile):
        while 1:
            uselessLine = bookFile.readline()
            if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                continue
            else:
                break
