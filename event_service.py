# event_service.py
from db import get_db

def get_all_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events")
    return cursor.fetchall()

def add_event(title, date, description, img, author, address, cost, register):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO events (title, date, description, img, author, adress, cost, register) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (title, date, description, img, author, address, cost, register))
    db.commit()


if __name__ == '__main__':
    print("nuh uh")
else:
    print("import event_service")