from flask import *
from sqlite3 import *
from database import *


app = Flask(__name__)

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email, password, lvl) VALUES (?, ?, ?, ?)", (name, email,password,0))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
