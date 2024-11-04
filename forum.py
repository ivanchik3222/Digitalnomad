from flask import render_template, request
from flask_login import current_user

from db import get_db

def forum():
    if request.method == 'POST':
        content = request.form['content']
        main_status = request.form['main_status']
        likes = 0
        owner_name = current_user.name
        owner_id = current_user.id

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (content, main_status, likes, owner_name, owner_id) VALUES (?, ?, ?, ?, ?)", (content, main_status, likes, owner_name, owner_id))
        db.commit()

    return render_template('forum.html')

if __name__ == '__main__':
    print("nuh uh")
else:
    print("import forum")