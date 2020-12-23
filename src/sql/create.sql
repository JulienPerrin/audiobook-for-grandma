CREATE TABLE IF NOT EXISTS BOOK(
    IDENTIFIER,
    FORMAT,
    NAME,
    TITLE,
    CREATOR,
    GENRE,
    DOWNLOADS,
    PUBLICDATE,
    PUBLISHER,
    VOLUME
);

CREATE TABLE IF NOT EXISTS BOOKMARK(
    IDENTIFIER,
    LINE_NUMBER
);

CREATE TABLE IF NOT EXISTS CONTINUE_READING(
    CONTINUE_READING,
    LAST_UPDATE, 
    IDENTIFIER
); 