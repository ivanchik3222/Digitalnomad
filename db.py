# db.py
from flask import g
import sqlite3

DATABASE = '/home/ivanchik322/Digitalnomad/database.db'

def get_db():
    """Connect to the database and return the connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    """Close the database connection when done."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()


        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            lvl INTEGER NOT NULL,
                            events TEXT,
                            sav_days TEXT,
                            friends TEXT,
                            profile_image BLOB)''')
        # cursor.execute("ALTER TABLE users ADD COLUMN ")


        cursor.execute('''CREATE TABLE IF NOT EXISTS events(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            date TEXT NOT NULL,
                            description TEXT NOT NULL,
                            img TEXT NOT NULL,
                            author TEXT NOT NULL,
                            adress TEXT NOT NULL,
                            register TEXT NOT NULL,
                            cost INTEGER,
                            type TEXT NOT NULL)''')


        cursor.execute('''CREATE TABLE IF NOT EXISTS topics (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id)
                        )''')


        cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT NOT NULL,
                            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                            user_id INTEGER NOT NULL,
                            topic_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id),
                            FOREIGN KEY (topic_id) REFERENCES topics(id)
                        )''')


        cursor.execute('''CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        website TEXT NOT NULL,
                        coordinates TEXT NOT NULL,
                        image_url TEXT NOT NULL,
                        qr_code_url TEXT NOT NULL
                    )''')

        db.commit()



if __name__ == '__main__':
    print("nuh uh")
else:
    print("import db")
