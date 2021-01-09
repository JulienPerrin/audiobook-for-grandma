# TODO

## On this project

### Minimum viable product

- [x] télécharger un livre
- [x] lire un livre
  - [x] with the right encoding
- [x] sauter le début inutile du livre
  - [x] skip until \*\*\* START OF THE GUTEMBERG PROJECT
- [x] choose the languages of the books to read
- [x] add a command to stop the readings, and another to resume the reading
  - [x] add the bookmark fonctionality
    - [x] save bookmark on DB
    - [x] when the app is stoped and restarted, start 5 lines before bookmark
- [x] add a command to skip to the next book
  - [x] get all the list of books
    - [x] save all books metadata
  - [x] suggestion algorithm for books
    - [x] base first suggestions on the number of downloads
    - [x] base suggestions on the percetage of the books read and their authors
    - [x] suggest based on book subject
  - [x] save skipped books and do not suggest them again
- [x] add a command to download all the database in a certain language for it to work offline

### Nice additional fonctionalities

- [x] find a way to kill current reading better than the actual stop option
- [ ] add a command to save book into favorites (too complicated ?)
  - [ ] add possiblity to remove from fav
  - [ ] add a command to read the favorites when the reading is stoped
- [x] reduce/increase volume
- [x] reduce/increase reading speed
- [ ] make voice configurable in options
- [x] option file 
- [ ] moove back or forward

## Rasperry Pi interface

- [x] code a script so that when a button connected to the raspberry is pushed, a command is executed on this project
- [x] how to connect buttons to the Raspberry Pi so that my grandma can push them
  - [x] 8BidDio controller connected to the Raspberry via USB
- [ ] write tutorial on how I did it
  - buy the Raspberry Pi and the 8BitDo controller (links ?)
  - flash Linux on Raspberry
  - install espeak
  - install mbrola voice : https://github.com/espeak-ng/espeak-ng/blob/master/docs/mbrola.md#installation-of-mbrola-package-from-source
  - install python3 and make python3 default
  - install make
  - pip install virtualenv wheel setuptools
  - virtualenv venv
  - clone the project on raspberry
  - explain how to update options:
    - default volume
    - default rate of speech
    - default voice
    - default language
  - add it as a service in systemctl
