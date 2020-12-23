import os
from os import listdir
from os.path import isfile, join

import playsound
import pyttsx3
import yaml
from gtts import gTTS
from pyttsx3 import engine

from .DB import DB
from .model.Book import Book
from .model.Bookmark import Bookmark


class BookReader():
    book: Book
    text: str
    engine: engine.Engine
    db: DB

    def __init__(self, db, languageTest='', rate=150):
        self.text = ''
        self.db = db
        self.engine = pyttsx3.init()
        self.engine.connect('started-word', self.onWord)
        if rate:
            self.engine.setProperty('rate', rate)
        if languageTest:
            self.engine.say(languageTest)

    def read(self) -> ():
        # tts = gTTS(text=self.text, lang="fr")
        # path = join('out', 'mp3', 'hello.mp3')
        # tts.save(path)
        # playsound.playsound(path)
        self.engine.say(self.text)
        self.engine.runAndWait()

    def readBook(self) -> ():
        # skip = 6999
        # nbToRead = 300

        self.text = ''
        print("path to file to read: ", self.book.pathOfFileToRead)
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
        with open(self.book.pathOfFileToRead) as bookFile:
            if hasGutenbergIntro:
                while 1:
                    uselessLine = bookFile.readline()
                    if uselessLine and not uselessLine.startswith('*** START OF THIS PROJECT GUTENBERG'):
                        continue
                    else:
                        break
            while self.db.isContinueReading():
                line = bookFile.readline().strip() + ' '
                if not line.strip():
                    continue
                sentenceChunks = line.split('.')
                i = 0
                for sentenceChunk in sentenceChunks:
                    if i==0 and len(sentenceChunks)>1:
                        # the begining of the sentence is on the previous line, the end is on this line
                        self.text += '{}. '.format(sentenceChunk)
                        self.read()
                        print("finished sentence: {}".format(self.text))
                    elif i==0:
                        # the begining of the sentence is on the previous line
                        self.text += '{} '.format(sentenceChunk)
                        print("updated sentence: {}".format(self.text))
                    elif i<len(sentenceChunks)-1:
                        # the entire sentence is on this line
                        self.text = '{}. '.format(sentenceChunk)
                        self.read()
                        print("sentence: {}".format(self.text))
                    else:
                        self.text = '{} '.format(sentenceChunk)
                        print("beginned sentence: {}".format(self.text))
                        # the end of the sentence is on the next line
                    i+=1
                # print("line {}: {}".format(self.book.bookmark.nextLine(), line))
                # if self.book.bookmark.lastLineRead > nbToRead:
                #     break
        self.read()

    def onWord(self, name, location, length):
        # print('word', name, location, length)
        if not self.db.isContinueReading():
            self.engine.stop()

