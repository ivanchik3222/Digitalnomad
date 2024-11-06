from flask import *
from flask_login import *

from db import get_db

def forum():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, created_at FROM topics ORDER BY created_at DESC")
    topics = cursor.fetchall()
    return render_template('forum.html', topics=topics)

@login_required
def new_topic():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO topics (title, content, user_id) VALUES (?, ?, ?)", 
                       (title, content, current_user.id))
        db.commit()
        flash("Тема успешно создана!", "success")
        return redirect(url_for('forum'))
    return redirect(url_for('forum'))

def topic(topic_id):
    db = get_db()
    cursor = db.cursor()

    # Получение информации о теме
    cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
    topic = cursor.fetchone()

    # Получение комментариев
    cursor.execute("SELECT * FROM comments WHERE topic_id = ? ORDER BY created_at ASC", (topic_id,))
    comments = cursor.fetchall()

    # Обработка формы добавления комментария
    if request.method == 'POST':
        content = request.form['content']
        cursor.execute("INSERT INTO comments (content, user_id, topic_id) VALUES (?, ?, ?)", 
                       (content, current_user.id, topic_id))
        db.commit()
        flash("Комментарий добавлен!", "success")
        return redirect('/forum/topic/' + str(topic_id))

    return render_template('topic.html', topic=topic, comments=comments)

if __name__ == '__main__':
    print("nuh uh")
else:
    print("import forum")