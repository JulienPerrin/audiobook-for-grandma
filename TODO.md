# TODO

## On this project

### Minimum viable product

- [x] télécharger un livre
- [x] lire un livre
- [x] sauter le début inutile du livre
  - [x] skip until *** START OF THE GUTEMBERG PROJECT
- [x] choose the languages of the books to read
- [x] add a command to stop the readings, and another to resume the reading
  - [x] add the bookmark fonctionality
    - [x] save bookmark on DB
    - [x] when the app is stoped and restarted, start 5 lines before bookmark
- [x] add a command to skip to the next book
  - [x] get all the list of books
  - [ ] suggestion algorithm for books
    - [ ] base first suggestions on the number of downloads
    - [ ] base suggestions on the percetage of the books read and their genre and authors
  - [x] save skipped books and do not suggest them again
- [ ] add a command to download all the database in a certain language for it to work offline

### Nice additional fonctionalities

- [ ] read the book without using the lazy method of iterating on all the lines
  - [ ] correctly manage unicode files
- [ ] add a command to save book into favorites
  - [ ] add possiblity to remove from fav
  - [ ] add a command to read the favorites when the reading is stoped
- [ ] add a command to go faster/slower
- [ ] reduce/increase volume
- [ ] reduce/increase reading speed
## Rasperry Pi interface

- [ ] code a script  so that when a button connected to the raspberry is pushed, a command is executed on this project
- [ ] how to connect electrical components to the Raspberry Pi so that my grandma can push them 
  - [ ] or use bluetooth
- [ ] write tutorial on how I did it

