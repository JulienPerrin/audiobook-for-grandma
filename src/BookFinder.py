import wget
import logging.config
import os
import yaml

from internetarchive import search_items, download

import os.path


class BookFinder():
    def __init__(self):
        self.url = 'http://www.futurecrew.com/skaven/song_files/mp3/razorback.mp3'

    def findBook(self) -> str:
        i = 0
        # '''https://archive.org/advancedsearch.php?q=collection%3A%28gutenberg%29+AND+mediatype%3A%28texts%29+AND+language%3A%28fr%29&fl%5B%5D=creator&fl%5B%5D=downloads&fl%5B%5D=format&fl%5B%5D=genre&fl%5B%5D=identifier&fl%5B%5D=name&fl%5B%5D=publicdate&fl%5B%5D=publisher&fl%5B%5D=title&fl%5B%5D=volume&sort%5B%5D=downloads+desc&sort%5B%5D=&sort%5B%5D=&rows=50&page=1&output=json&callback=callback&save=yes#raw'''
        for item in search_items(query='collection:(gutenberg) AND mediatype:(texts) AND language:(fr)'):
            print("item " + str(i) + ": " + str(item))
            download(item['identifier'], destdir='out/gutenberg', verbose=True, checksum=True, glob_pattern='*txt', ignore_existing=True)
            if (i<2):
                break
        #download('lantijustineoule26804gut', destdir='out/gutenberg', verbose=True, checksum=True, glob_pattern='*txt', ignore_existing=True)
        return '''Apr�s la M�diterran�e, qu'il regarde comme la plus agr�able partie de
la mer, � cause de la temp�rature de l'air et de ses autres avantages,
il loue cette partie de l'Oc�an, o� r�gnent particuli�rement les vents
alis�s, parce qu'� certaine distance de la terre, on n'y trouve point
de grosses mers ni d'orages dangereux, et que les jours et les nuits y
sont d'une longueur �gale. Telles sont les mers plac�es sous la zone
torride. '''

