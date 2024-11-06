# auth_service.py
import base64
import io
import os
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from auth_models import User
from flask  import *
from flask_login import current_user


def authenticate_user(email, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    if user_data and check_password_hash(user_data[3], password):
        return User(user_data[0], user_data[1], user_data[2])
    return None

def register_user(name, email, password):
    """Register a new user in the database."""
    db = get_db()
    cursor = db.cursor()
    
    # Проверка, существует ли уже пользователь с таким email
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone() is not None:
        return False  # Email уже существует
    
    # Хешируем пароль и добавляем пользователя в базу данных
# Задаем абсолютный путь к файлу




# Проверяем наличие файла и читаем его

    with open('/home/ivanchik322/Digitalnomad/static/img/-1.png', 'rb') as file:
        default_image_data = file.read()




    # Хешируем пароль и добавляем пользователя в базу с изображением
    hashed_password = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO users (name, email, password, lvl, profile_image) 
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, hashed_password, 0, default_image_data))
    
    db.commit()
    return True


def get_user_by_id(user_id):
    """Retrieve a user from the database by ID."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])  # Создаем объект пользователя
    return None

def current_profile_image():
    if not current_user.is_authenticated:
        return send_file('static/img/-1.png', mimetype="image/png")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT profile_image FROM users WHERE id = ?", (current_user.id,))
    user_data = cursor.fetchone()
    if user_data:
        image_stream = io.BytesIO(user_data[0])
        return send_file(image_stream, mimetype="image/png")

if __name__ == '__main__':
    print("nuh uh")
else:
    print("import auth_service")