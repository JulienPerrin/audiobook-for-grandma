SELECT IDENTIFIER, TITLE, CREATOR, DOWNLOADS, PUBLISHER, VOLUME, ENCODING FROM (
    SELECT IDENTIFIER, TITLE, CREATOR, DOWNLOADS, PUBLISHER, VOLUME, ENCODING, 
        (CASE WHEN LIKES_AND_DISLIKES IS NULL THEN 0 ELSE LIKES_AND_DISLIKES END) AS SCORE
    FROM (
        SELECT book.IDENTIFIER, book.TITLE, book.CREATOR, book.DOWNLOADS, book.PUBLISHER, book.VOLUME, book.ENCODING, 
            (
                SELECT SUM(
                    CASE 
                        WHEN bookmarkSameAuthor.LINE_NUMBER * 100 > bookmarkSameAuthor.TOTAL_LINES * 95 
                            THEN 1
                        WHEN bookmarkSameAuthor.SKIPPED = 1 
                            AND bookmarkSameAuthor.LINE_NUMBER * 100 < bookmarkSameAuthor.TOTAL_LINES * 5 
                            THEN -1
                        ELSE 0
                    END
                )
                FROM BOOK bookSameAuthor
                JOIN BOOKMARK bookmarkSameAuthor ON bookSameAuthor.IDENTIFIER = bookmarkSameAuthor.IDENTIFIER
                WHERE bookSameAuthor.CREATOR = book.CREATOR
            ) AS LIKES_AND_DISLIKES
        FROM BOOK book
        LEFT JOIN BOOKMARK bookmark ON bookmark.IDENTIFIER = book.IDENTIFIER
        WHERE (bookmark.SKIPPED IS NULL OR bookmark.SKIPPED = 0) AND (bookmark.FINISHED IS NULL OR bookmark.FINISHED = 0)
    )
    ORDER BY SCORE DESC, VOLUME DESC, DOWNLOADS DESC
);