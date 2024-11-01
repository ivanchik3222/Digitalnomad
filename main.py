from flask import *
from flask_login import *
from werkzeug.security import *
import sqlite3



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
DATABASE = 'database.db'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to this route for login

def get_db():
    """Connect to the database and return the connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    """Initialize the database and create tables."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Create the users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            lvl INTEGER NOT NULL,
                            events TEXT,
                            sav_days TEXT,
                            friends TEXT)''')

        # Create the events table
        cursor.execute('''CREATE TABLE IF NOT EXISTS events(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            date TEXT NOT NULL,
                            description TEXT NOT NULL,
                            img TEXT NOT NULL,
                            author TEXT NOT NULL,
                            adress TEXT NOT NULL,
                            register TEXT NOT NULL,
                            cost INTEGER)''')


        cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            owner TEXT NOT NULL)''')

        # Create the repairs table
        # cursor.execute('''CREATE TABLE IF NOT EXISTS repairs(
        #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                     title TEXT NOT NULL,
        #                     description TEXT NOT NULL,
        #                     adress TEXT NOT NULL,
        #                     date TEXT NOT NULL)''')

        # # Create the voitings table
        # cursor.execute('''CREATE TABLE IF NOT EXISTS voitings(
        #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                     title TEXT NOT NULL,
        #                     author INTEGER NOT NULL,
        #                     variants TEXT NOT NULL,
        #                     results TEXT NOT NULL,
        #                     voiters TEXT NOT NULL)''')
        
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection when done."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class User(UserMixin):
    """User model for Flask-Login."""
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    """Load a user by their ID."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        
        # Check if the email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('Email address already exists.')
            return redirect(url_for('register'))

        # Hash the password and save the user to the database
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (name, email, password, lvl) VALUES (?, ?, ?, ?)", (name, email, hashed_password, 0))
        db.commit()

        flash('Registration successful! You can now log in.')
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user_data = cursor.fetchone()
        if user_data and check_password_hash(user_data[3], password):  # Check hashed password
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Log out the user."""
    logout_user()
    return redirect('/')

# @app.route('/add_user', methods=['POST'])
# def add_user():
#     """Add a new user to the database."""
#     name = request.form['name']
#     email = request.form['email']
#     password = generate_password_hash(request.form['password'])  # Hash the password
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("INSERT INTO users (name, email, password, lvl) VALUES (?, ?, ?, ?)", (name, email, password, 0))
#     db.commit()
#     return redirect('/')

@app.route('/add_event', methods=['POST', 'GET'])
def add_event():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            description = request.form['description']
            img = request.form['image']
            author = current_user.name
            adress = request.form['location']
            cost = request.form['price']
            register = request.form['register']
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO events (title, date, description, img, author, adress, cost,register) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, date, description, img, author, adress, cost,register))
            db.commit()
            return redirect('/')
        return render_template('add_event.html')

@app.route('/', methods=['GET'])
def events():
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()
    return render_template('events.html', events=events , comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        title = request.form['title']
        content = request.form['content']
        owner = current_user.name
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO comments (title, content, owner) VALUES (?, ?, ?)", (title, content, owner))
        db.commit()
        return redirect('/')

@app.route('/event/<id>', methods=['GET'])
def event(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (id,))
    event = cursor.fetchone()
    print(event)
    if event is not None:
        return render_template('event.html', event=event)
    else:
        return "not found"
    
@app.route('/extra', methods=['GET'])
def extreme():
    return render_template('extra.html')

@app.route('/services', methods=['GET'])
def services():
    return render_template('services.html')


@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
