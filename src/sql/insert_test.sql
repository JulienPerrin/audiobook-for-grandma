DELETE FROM BOOKMARK;
INSERT INTO BOOK (
        IDENTIFIER,
        TITLE,
        CREATOR,
        DOWNLOADS,
        PUBLISHER,
        VOLUME,
        ENCODING
    )
VALUES (
        'abrgdelhistoireg38256gut',
        'Abrégé de l''Histoire Générale des Voyages (Tome 3)',
        'Jean-François de La Harpe',
        '26',
        'Project Gutenberg',
        NULL,
        'ISO-8859-1'
    ),
    (
        'abrgdelhistoireg38257gut',
        'Abrégé de l''Histoire Générale des Voyages (Tome 4)',
        'Jean-François de La Harpe',
        '31',
        'Project Gutenberg',
        NULL,
        'ISO-8859-1'
    );
INSERT INTO BOOKMARK (
        IDENTIFIER,
        LINE_NUMBER,
        TOTAL_LINES,
        SKIPPED,
        FINISHED
    )
VALUES ('abrgdelhistoireg38256gut', 9000, 9000, 0, 1),
    ('abrgdelhistoireg38257gut', 9208, 9213, 0, 0);
INSERT INTO CONTINUE_READING (IDENTIFIER, LAST_UPDATE, CONTINUE_READING)
VALUES (
        'abrgdelhistoireg38257gut',
        strftime('%s', 'now'),
        1
    );