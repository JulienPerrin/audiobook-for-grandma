import os
from os.path import join

import chardet
from chardet.universaldetector import UniversalDetector

import pyttsx3
from pyttsx3 import engine

from .DB import DB
from .model.Book import Book


class BookReader():
    book: Book
    textToRead: str
    engine: engine.Engine
    db: DB
    rate: int
    volume: float

    def __init__(self, db, languageTest='', rate: int = 150, volume=0.5):
        self.textToRead = ''
        self.db = db
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume
        voices = [(voice.name, voice.id) for voice in self.engine.getProperty('voices')]
        print("engine voices", voices)
        self.engine.setProperty('voice', 'mb-fr4')
        if rate:
            self.engine.setProperty('rate', int(self.rate))
        if volume:
            self.engine.setProperty('volume', float(self.volume))
        self.engine.connect('started-word', self.onWord)
        if languageTest:
            self.engine.say(languageTest)

    def read(self) -> ():
        self.engine.say(self.textToRead)
        self.engine.runAndWait()
        self.textToRead = ''

    def readBook(self, book: Book) -> ():
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
            self.db.updateBookmark(identifier=self.book.identifier, lastLineRead=lineNumber, numberOfLines=self.countFileLines())
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
                fullLine = bookFile.readline()
                if not fullLine:
                    self.db.markFinished()
                line = fullLine.strip() + ' '
                lineNumber += 1
                # print("line {}: {}".format(lineNumber, line))
                if not line.strip():
                    continue
                sentenceChunks = line.split('.')
                i = 0
                for sentenceChunk in sentenceChunks:
                    textStripped = sentenceChunk.strip()
                    if textStripped:
                        if i == 0 and len(sentenceChunks) > 1:
                            # the begining of the sentence is on the previous line, the end is on this line
                            self.textToRead += '{}. '.format(textStripped)
                            print("finished sentence: {}".format(self.textToRead))
                            self.db.updateBookmark(identifier=self.book.identifier, lastLineRead=lineNumber)
                            self.read()
                        elif i == 0:
                            # the begining of the sentence is on the previous line
                            self.textToRead += '{} '.format(textStripped)
                            # print("updated sentence: {}".format(self.textToRead))
                        elif i < len(sentenceChunks)-1:
                            # the entire sentence is on this line
                            self.textToRead = '{}. '.format(textStripped)
                            print("sentence: {}".format(self.textToRead))
                            self.read()
                        else:
                            # the end of the sentence is on the next line
                            self.textToRead = '{} '.format(textStripped)
                            # print("beginned sentence: {}".format(self.textToRead))
                    i += 1
            # read the last sentence if it does not end with a point
            if (self.db.isFinished(self.book.identifier)):
                self.read()
            print('\n')

    def onWord(self, name, location, length):
        if not self.db.isContinueReading():
            self.engine.stop()

    def detectFileEncoding(self) -> ():
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
            return sum([1 for i in bookFileWithLinesToCount])

    def hasGutenbergIntro(self):
        hasGutenbergIntro = False
        with open(self.book.pathOfFileToRead, encoding=self.book.encoding) as bookFile:
            uselessLineIndex = 500
            while 1:
                uselessLine = bookFile.readline()
                if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                    hasGutenbergIntro = True
                uselessLineIndex += 1
                if (uselessLineIndex > 500):
                    break
        return hasGutenbergIntro

    def skipGutenbergIntro(self, bookFile):
        while 1:
            uselessLine = bookFile.readline()
            if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                continue
            else:
                break
