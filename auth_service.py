# auth_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from auth_models import User


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
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (name, email, password, lvl) VALUES (?, ?, ?, ?)", 
                   (name, email, hashed_password, 0))
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