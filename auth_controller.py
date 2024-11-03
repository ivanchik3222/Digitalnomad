# auth_controller.py
from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user
from auth_service import register_user, authenticate_user

def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Пытаемся зарегистрировать пользователя
        if register_user(name, email, password):
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))  # Перенаправление на страницу входа после регистрации
        else:
            flash('Email address already exists. Please use a different email.')
            return redirect(url_for('register'))
    
    return render_template('register.html')

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)
        if user:
            login_user(user)
            return redirect(url_for('events'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))
