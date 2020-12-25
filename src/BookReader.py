import os
from os import listdir
from os.path import isfile, join

import pyttsx3
import yaml
from pyttsx3 import engine

from .DB import DB
from .model.Book import Book

# from gtts import gTTS
# import playsound


class BookReader():
    book: Book
    text: str
    engine: engine.Engine
    db: DB
    rate: int
    volume: float

    def __init__(self, db, languageTest='', rate: int = 150, volume=0.5):
        self.text = ''
        self.db = db
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume
        print("engine voices", [(voice.name, voice.id)
                                for voice in self.engine.getProperty('voices')])
        if rate:
            self.engine.setProperty('rate', int(self.rate))
        if volume:
            self.engine.setProperty('volume', float(self.volume))
        self.engine.connect('started-word', self.onWord)
        if languageTest:
            self.engine.say(languageTest)

    def read(self) -> ():
        # tts = gTTS(text=self.text, lang="fr")
        # path = join('out', 'mp3', 'hello.mp3')
        # tts.save(path)
        # playsound.playsound(path)
        self.engine.say(self.text)
        self.engine.runAndWait()
        self.text = ''

    def readBook(self, book: Book) -> ():
        self.book = book
        self.text = ''
        # print("path to file to read: ", self.book.pathOfFileToRead)

        self.db.updateContinueReading(True, self.book.identifier)
        lineNumber = self.db.getBookmark(self.book.identifier)
        numberOfLines = None
        if lineNumber is None:
            with open(self.book.pathOfFileToRead) as bookFileWithLinesToCount:
                numberOfLines = sum([1 for i in bookFileWithLinesToCount])
            lineNumber = 0
        with open(self.book.pathOfFileToRead) as bookFile:
            # if the gutenberg intro is at the beginning of the file, then remove it if we have not already started reading the book
            if self.hasGutenbergIntro() and lineNumber == 0:
                while 1:
                    uselessLine = bookFile.readline()
                    if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                        continue
                    else:
                        break
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
                            self.text += '{}. '.format(textStripped)
                            print("finished sentence: {}".format(self.text))
                            self.db.updateBookmark(
                                identifier=self.book.identifier, lastLineRead=lineNumber, numberOfLines=numberOfLines)
                            self.read()
                        elif i == 0:
                            # the begining of the sentence is on the previous line
                            self.text += '{} '.format(textStripped)
                            # print("updated sentence: {}".format(self.text))
                        elif i < len(sentenceChunks)-1:
                            # the entire sentence is on this line
                            self.text = '{}. '.format(textStripped)
                            print("sentence: {}".format(self.text))
                            self.read()
                        else:
                            # the end of the sentence is on the next line
                            self.text = '{} '.format(textStripped)
                            # print("beginned sentence: {}".format(self.text))
                    i += 1

    def onWord(self, name, location, length):
        if not self.db.isContinueReading():
            self.engine.stop()

    def hasGutenbergIntro(self):
        hasGutenbergIntro = False
        with open(self.book.pathOfFileToRead) as bookFile:
            uselessLineIndex = 500
            while 1:
                uselessLine = bookFile.readline()
                if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                    hasGutenbergIntro = True
                uselessLineIndex += 1
                if (uselessLineIndex > 500):
                    break
        return hasGutenbergIntro
