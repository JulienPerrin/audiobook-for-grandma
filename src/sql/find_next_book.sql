SELECT IDENTIFIER, TITLE, CREATOR, DOWNLOADS, PUBLISHER, VOLUME, ENCODING FROM (
    SELECT IDENTIFIER, TITLE, CREATOR, DOWNLOADS, PUBLISHER, VOLUME, ENCODING, 
        (SCORE_AUTHOR * 5 + SCORE_SUBJECT) AS SCORE
    FROM (
        SELECT IDENTIFIER, TITLE, CREATOR, DOWNLOADS, PUBLISHER, VOLUME, ENCODING, 
            (CASE WHEN AUTHOR_LIKES_AND_DISLIKES IS NULL THEN 0 ELSE AUTHOR_LIKES_AND_DISLIKES END) AS SCORE_AUTHOR,
            (CASE WHEN SUBJECT_LIKES_AND_DISLIKES IS NULL THEN 0 ELSE SUBJECT_LIKES_AND_DISLIKES END) AS SCORE_SUBJECT
        FROM (
            SELECT book.IDENTIFIER, book.TITLE, book.CREATOR, book.DOWNLOADS, book.PUBLISHER, book.VOLUME, book.ENCODING, 
                (
                    SELECT SUM(
                        CASE 
                            --a book is liked if gradma read more thant 95% of it
                            WHEN bookmarkSameAuthor.LINE_NUMBER * 100 > bookmarkSameAuthor.TOTAL_LINES * 95 
                                THEN 1
                            --a book is disliked if gradma read less than 5% of it and skipped it
                            WHEN bookmarkSameAuthor.SKIPPED = 1 
                                AND bookmarkSameAuthor.LINE_NUMBER * 100 < bookmarkSameAuthor.TOTAL_LINES * 5 
                                THEN -1
                            ELSE 0
                        END
                    )
                    FROM BOOK bookSameAuthor
                    JOIN BOOKMARK bookmarkSameAuthor ON bookSameAuthor.IDENTIFIER = bookmarkSameAuthor.IDENTIFIER
                    WHERE bookSameAuthor.CREATOR = book.CREATOR
                ) AS AUTHOR_LIKES_AND_DISLIKES,
                (
                    SELECT SUM(
                        CASE 
                            --a book is liked if gradma read more thant 95% of it
                            WHEN bookmarkSameSubject.LINE_NUMBER * 100 > bookmarkSameSubject.TOTAL_LINES * 95 
                                THEN 1
                            --a book is disliked if gradma read less than 5% of it and skipped it
                            WHEN bookmarkSameSubject.SKIPPED = 1 
                                AND bookmarkSameSubject.LINE_NUMBER * 100 < bookmarkSameSubject.TOTAL_LINES * 5 
                                THEN -1
                            ELSE 0
                        END
                    )
                    FROM SUBJECT subject 
                    JOIN BOOKMARK bookmarkSameSubject ON subject.IDENTIFIER = bookmarkSameSubject.IDENTIFIER
                    WHERE subject.NAME IN (SELECT sameSubject.NAME FROM SUBJECT sameSubject WHERE book.IDENTIFIER = sameSubject.IDENTIFIER)
                ) AS SUBJECT_LIKES_AND_DISLIKES
            FROM BOOK book
            LEFT JOIN BOOKMARK bookmark ON bookmark.IDENTIFIER = book.IDENTIFIER
            WHERE (bookmark.SKIPPED IS NULL OR bookmark.SKIPPED = 0) AND (bookmark.FINISHED IS NULL OR bookmark.FINISHED = 0)
        ) ORDER BY SCORE_AUTHOR DESC, SCORE_SUBJECT DESC, VOLUME DESC, DOWNLOADS DESC
    ) ORDER BY SCORE DESC, VOLUME DESC, DOWNLOADS DESC
);