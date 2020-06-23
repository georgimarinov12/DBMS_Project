import sqlite3 as sqlite


DB_NAME = "MAL.db"

conn = sqlite.connect(DB_NAME)


conn.cursor().execute('''
PRAGMA foreign_keys = ON;
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS anime
    (
        title TEXT NOT NULL,
        image BLOB NOT NULL,
        studio TEXT NOT NULL,
        episodes INTEGER NOT NULL,
        seasons INTEGER NOT NULL,
        anime_id INTEGER PRIMARY KEY AUTOINCREMENT
    )
''')
conn.commit()


conn.cursor().execute('''
PRAGMA foreign_keys = ON;
''')
conn.commit()

conn.cursor().execute('''

CREATE TABLE IF NOT EXISTS characters
    (
        name TEXT NOT NULL UNIQUE,
        image BLOB NOT NULL,
        anime TEXT NOT NULL,
        VA TEXT NOT NULL,
        character_id INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY(anime) REFERENCES anime(title) ON DELETE CASCADE,
        FOREIGN KEY(VA) REFERENCES VAs(name) ON DELETE CASCADE
    )
''')
conn.commit()


conn.cursor().execute('''
PRAGMA foreign_keys = ON;
''')
conn.commit()

conn.cursor().execute('''

CREATE TABLE IF NOT EXISTS VAs
    (
        name TEXT NOT NULL UNIQUE,
        image BLOB NOT NULL,
        VA_id INTEGER PRIMARY KEY AUTOINCREMENT
    )
''')
conn.commit()

class SQLite(object):

    def __enter__(self):
        self.conn = sqlite.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
