import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    # Подключаемся к базе данных
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    # Инициализируем базу данных и создаем таблицы
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            lvl INTEGER NOT NULL,
                            events TEXT,
                            sav_days TEXT,
                            friends TEXT
                        )''')
                       
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS events(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            date TEXT NOT NULL,
                            description TEXT NOT NULL,
                            img TEXT NOT NULL,
                            author TEXT NOT NULL,
                            adress TEXT NOT NULL
                        )''')
                       

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS repairs(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            adress TEXT NOT NULL,
                            date TEXT NOT NULL
                       )''')
        

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS voitings(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            author INTEGER NOT NULL,
                            variants TEXT NOT NULL,
                            results TEXT NOT NULL,
                            voiters TEXT NOT NULL
                       )''')
        db.commit()



@app.teardown_appcontext
def close_connection(exception):
    # Закрываем соединение с базой данных
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    print("nuh uh")
else:
    print("successfull import")
