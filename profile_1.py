# profile.py
import base64
import sqlite3
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from db import get_db
import os
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@login_required
def profile():
    """Страница профиля текущего пользователя"""
    db = get_db()
    db.row_factory = sqlite3.Row 
    cursor = db.cursor()

    # Получаем информацию о текущем пользователе через current_user
    cursor.execute("SELECT * FROM users WHERE id = ?", (current_user.id,))
    user = cursor.fetchone()

    # Конвертируем изображение в base64, если оно хранится как BLOB
    profile_image = None
    if user['profile_image']:
        profile_image = base64.b64encode(user['profile_image']).decode('utf-8')


    return render_template('profile.html', user=user, profile_image=profile_image)

@login_required
def set_profile():

    """Редактирование профиля текущего пользователя"""
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        # Обновление данных в базе
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, current_user.id))
        db.commit()
        flash("Профиль успешно обновлен")
        return redirect(url_for('profile'))
    
    db = get_db()
    cursor = db.cursor()

    # Получаем информацию о текущем пользователе через current_user
    cursor.execute("SELECT * FROM users WHERE id = ?", (current_user.id,))
    user = cursor.fetchone()  # Возвращается как sqlite3.Row, благодаря db.row_factory

    # Передаем данные пользователя в шаблон
    return render_template('red_profile.html', user=user)

@login_required
def update_profile():
    db = get_db()
    cursor = db.cursor()

    # Получаем информацию о текущем пользователе через current_user
    cursor.execute("SELECT * FROM users WHERE id = ?", (current_user.id,))
    user = cursor.fetchone() 
    """Обработка формы обновления профиля текущего пользователя"""
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        rank = request.form['rank']

        # Обновление данных пользователя в базе
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE users 
            SET name = ?, email = ?, sav_days = ?, lvl = ? 
            WHERE id = ?
        """, (name, email, phone, rank, current_user.id))
        db.commit()
        
        flash("Профиль успешно обновлен")
        return redirect(url_for('profile'))

    # Отображаем форму редактирования профиля, если метод запроса не POST
    return redirect(url_for('red_profile'))




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
def upload_profile_image():
    """Маршрут для загрузки и сохранения изображения профиля"""
    if 'file' not in request.files:
        flash('Файл не найден.')
        return redirect(url_for('profile'))

    file = request.files['file']

    if file.filename == '':
        flash('Файл не выбран.')
        return redirect(url_for('profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Читаем файл как бинарные данные
        img_data = file.read()

        # Проверка на случай отсутствия данных в файле
        if img_data is None:
            flash('Ошибка загрузки изображения.')
            return redirect(url_for('profile'))

        # Сохраняем бинарные данные изображения в базе данных
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET profile_image = ? WHERE id = ?", (img_data, current_user.id))
        db.commit()

        flash('Изображение профиля успешно загружено.')
        return redirect(url_for('profile'))
    else:
        flash('Неверный формат файла. Разрешены только изображения.')
        return redirect(url_for('profile'))


if __name__ == '__main__':
    print("nuh uh")
else:
    print("import profile")
