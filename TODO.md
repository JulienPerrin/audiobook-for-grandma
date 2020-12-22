# TODO

## Minimum viable product

- [x] télécharger un livre
- [x] lire un livre
- [x] sauter le début inutile du livre
  - [x] skip until *** START OF THE GUTEMBERG PROJECT
- [x] choose the languages of the books to read
- [ ] add a command to stop the readings, and another to resume the reading
  - [ ] add the bookmark fonctionality
    - [ ] save bookmark on external file
    - [ ] when the app is stoped and restarted, start to read on bookmark
- [ ] add a command to skip to the next book
  - [ ] get all the list of books
  - [ ] suggestion algorithm for books
    - [ ] base first suggestions on the number of downloads
    - [ ] take into account what the user likes and dislikes 
  - [ ] save skipped books and do not suggest them again
- [ ] add a command to download all the database in a certain language for it to work offline

## Nice additional fonctionalities

- [ ] read the book without using the lazy method of iterating on all the lines
  - [ ] correctly manage unicode files
- [ ] add a command to save book into favorites
  - [ ] add possiblity to remove from fav
  - [ ] add a command to read the favorites when the reading is stoped
