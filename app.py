# app.py
from flask import Flask
from flask_login import LoginManager
from db import close_connection
from auth_controller import register, login, logout
from auth_service import get_user_by_id
from event_controller import events, add_event, add_event_route
from auth_models import User

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.teardown_appcontext(close_connection)

# Начальные настройки
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# URL для регистрации\входа
app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=logout)

# URL для событий
app.add_url_rule('/', view_func=events)
app.add_url_rule('/add_event', view_func=events, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
