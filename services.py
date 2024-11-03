import sqlite3
from flask import request, redirect, url_for, flash, render_template
from db import get_db

def services():
    db = get_db()
    db.row_factory = sqlite3.Row 
    cursor = db.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    print(services)
    return render_template('services.html', services=services)


def add_service():
    if request.method == 'POST':
    # Получаем данные из формы
        name = request.form['name']
        description = request.form['description']
        phone = request.form['phone']
        website = request.form['website']
        coordinates = request.form['coordinates']
        image_url = request.form['image_url']
        qr_code_url = request.form['qr_code_url']

        # Сохраняем данные в базе данных
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO services (name, description, phone, website, coordinates, image_url, qr_code_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, description, phone, website, coordinates, image_url, qr_code_url))
        db.commit()

        flash("Услуга успешно добавлена!")
        return redirect(url_for('services'))
    return render_template('add_service.html')


if __name__ == '__main__':
    print("nuh uh")
else:
    print("import services")