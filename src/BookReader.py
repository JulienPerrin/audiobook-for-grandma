import os
from os import listdir
from os.path import isfile, join

import playsound
import yaml
from gtts import gTTS

from .model.Book import Book
from .model.Bookmark import Bookmark

import pyttsx3
from pyttsx3 import engine


class BookReader():
    book: Book
    text: str
    engine: engine.Engine
    continueReading: bool

    def readText(self, text: str) -> ():
        self.text = text
        self.read()

    def read(self) -> ():
        # tts = gTTS(text=self.text, lang="fr")
        # path = join('out', 'mp3', 'hello.mp3')
        # tts.save(path)
        # playsound.playsound(path)
        self.engine.say(self.text)
        self.engine.runAndWait()

    def readBook(self) -> ():
        skip = 6999
        nbToRead = 1

        self.text = ''
        print("path to file to read: ", self.book.pathOfFileToRead)
        with open(self.book.pathOfFileToRead) as bookFile:
            while 1:
                uselessLine = bookFile.readline()
                if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                    continue
                else:
                    break
            # skip 150 line to avoid english text
            while skip > 0:
                skip -= 1
                bookFile.readline()
            while 1:
                # for now, read the firts 10 lines of this book
                line = bookFile.readline().strip() + ' '
                if not line.strip():
                    # if the line is blank, skip
                    continue
                self.text += line
                print("line ", self.book.bookmark.nextLine(), ": ", line)
                if self.book.bookmark.lastLineRead > nbToRead:
                    break
        self.read()

    def stopReading(self):
        self.continueReading = False

    def onWord(self, name, location, length):
        print('word', name, location, length)
        if not self.continueReading:
            self.engine.stop()

    def __init__(self, languageTest=''):
        self.text = ''
        self.continueReading = True
        self.engine = pyttsx3.init()
        self.engine.connect('started-word', self.onWord)
        self.engine.setProperty('rate', 200)
