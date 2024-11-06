# event_service.py
from db import get_db

def get_all_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events")
    return cursor.fetchall()

def get_sort_events(sort):
    if sort == "all":
        return get_all_events()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events WHERE type = ?", (sort,))
    return cursor.fetchall()

def add_event(title, date, description, img, author, address, cost, register, type):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO events (title, date, description, img, author, adress, cost, register, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (title, date, description, img, author, address, cost, register, type))
    db.commit()


if __name__ == '__main__':
    print("nuh uh")
else:
    print("import event_service")