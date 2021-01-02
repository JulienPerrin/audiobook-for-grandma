SELECT cr.CONTINUE_READING, bookmark.*, book.ENCODING, book.CREATOR, book.DOWNLOADS
FROM BOOKMARK bookmark 
LEFT JOIN BOOk book ON book.IDENTIFIER = bookmark.IDENTIFIER
LEFT JOIN CONTINUE_READING cr ON cr.IDENTIFIER = BOOK.IDENTIFIER
;