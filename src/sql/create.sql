CREATE TABLE IF NOT EXISTS BOOK(
    identifier,
    format,
    name,
    title,
    creator,
    genre,
    downloads,
    publicdate,
    publisher,
    volume
);

CREATE TABLE IF NOT EXISTS BOOKMARK(
    identifier,
    line_number
);

CREATE TABLE IF NOT EXISTS CONTINUE_READING(
    CONTINUE_READING,
    LAST_UPDATE
);