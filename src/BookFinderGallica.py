import os
from datetime import datetime
from os import listdir
from os.path import isfile, join

import requests

from .BookFinder import BookFinder
from .DB import DB
from .model.Book import Book

import xml.etree.cElementTree as ET

import re
import zipfile
from os import listdir
from os.path import isdir, isfile, join

import ebooklib
import yaml
from bs4 import BeautifulSoup
from ebooklib import epub
from ebooklib.utils import debug

class BookFinderGallica(BookFinder):

    def __init__(self, db, language='fr'):
        super().__init__(db, 'Gallica_direct', language='fr')
        if not self.db.isBookListDownloadedForPublisher(self.publisher):
            self.downloadBookList()

    def downloadBookList(self) -> None:
        startRecord = 0
        maximumRecords = 50
        END_POINT = 'https://gallica.bnf.fr/services/engine/search/opds'
        basic_params = {
            'query': 'sdewey+all+"84")+and+dc.format+adj+"Format+adaptable"+and+dc.format+all+"epub"',
            'startRecord': startRecord,
            'maximumRecords': maximumRecords,
        }
        result = requests.get(END_POINT, basic_params)
        print("result : {}".format(result))
        while True:
            if result.status_code == 200:
                feed = ET.fromstring(result.content)

                pageSuivante = feed.find('./{http://www.w3.org/2005/Atom}link[@rel="next"]').attrib["href"]
                totalResults = feed.findtext('./{http://a9.com/-/spec/opensearch/1.1/}totalResults')
                itemsPerPage = feed.findtext('./{http://a9.com/-/spec/opensearch/1.1/}itemsPerPage')
                startIndex = feed.findtext('./{http://a9.com/-/spec/opensearch/1.1/}startIndex')
                
                for entry in feed.findall('./{http://www.w3.org/2005/Atom}entry'):
                    if entry.findtext('./{http://www.w3.org/2005/Atom}id') == None:
                        continue
                    href = entry.find('./{http://www.w3.org/2005/Atom}link[@rel="http://opds-spec.org/acquisition"][@type="application/epub+zip"]').attrib['href']
                    if href == None:
                        continue
                    self.downloadBook(Book(
                        identifier=entry.findtext('./{http://www.w3.org/2005/Atom}id').split('/')[-1],
                        downloads=20,
                        creator=entry.findtext('./{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name'),
                        title=entry.findtext('./{http://www.w3.org/2005/Atom}title'),
                        publisher=self.publisher,
                        volume='',
                        downloaded=True,
                        encoding='utf-8',
                        href=href,
                    ))
                if startIndex + itemsPerPage <= totalResults:
                    result = requests.get(pageSuivante, {})
                else:
                    break
            else:
                break


    def downloadBook(self, book: Book) -> None:
        # download epub
        r = requests.get(book.href)
        gallicaDir = join('out', 'gallica')
        if not os.path.exists(gallicaDir):
            os.makedirs(gallicaDir, 777)
        destdir=join(gallicaDir, book.identifier)
        if not os.path.exists(destdir):
            os.makedirs(destdir, 777)
        
        filename = os.path.join(destdir, '{}.epub'.format(book.identifier))
        if not os.path.exists(filename):
            with open(filename,'wb') as output_file:
                output_file.write(r.content)

        #generate txt file and extract metadata
        self.epubToTxt(book, destdir, filename)

        if (book.downloaded):
            self.db.addBooks([book])
            print(datetime.now(), 'Book downloaded:', book)
        else:
            print(datetime.now(), 'Book not downloaded ! ', book)

    def epubToTxt(self, book: Book, destdir: str, filename: str):
        try:
            ebook = epub.read_epub(filename)
        except epub.EpubException:
            book.downloaded = False
            return

        book.subjects = []
        for sujet in ebook.get_metadata('DC', 'subject'):
            book.subjects.append(sujet[0])

        XHTML = '.xhtml'
        # https://gist.github.com/anotherdirtbag/7edf6780c962f9b09b929b59ad8501c2#file-epub_to_tts-py-L197
        with open(os.path.join(destdir, "{}.txt".format(book.identifier)), 'w', encoding='utf-8') as foutput:
            with zipfile.ZipFile(filename) as zip:
                zipfilenames = []
                for somename in zip.namelist():
                    if str(somename)[-len(XHTML):] == XHTML:
                        zipfilenames.append(str(somename)[:-len(XHTML)])
                # zipfilenames.sort()
                for chapterfilename in zipfilenames:
                    ftxt = zip.read(chapterfilename + XHTML)
                    soup = BeautifulSoup(ftxt, 'html.parser')
                    chaptertext = self.parseepubtext(soup)

                    foutput.write(chaptertext)

    def parseepubtext(self, soup):
        chaptertext = ''
        for line in soup.select('p'):
            chaptertext += str(line.get_text()).strip() + '\n'
        # remove page numbers
        chaptertext = re.sub(r'\n\d+\n', '\n', chaptertext)
        return chaptertext
        # this worked for the epub file i had, but the formatting is likely different for others.


