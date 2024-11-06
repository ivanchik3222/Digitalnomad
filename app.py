# app.py
from flask import Flask
from flask_login import LoginManager

from db import close_connection, init_db

from auth_controller import register, login, logout
from auth_service import get_user_by_id, current_profile_image

from event_controller import events, add_event, add_event_route, add_event_form, event_show, sorted_events

from event_service import get_sort_events
from static_routes import resources, extra

from services import services, add_service

from forum import forum, topic, new_topic

from profile_1 import profile, set_profile, update_profile, upload_profile_image

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
app.add_url_rule('/add_event', view_func=add_event_form, methods=['GET'])
app.add_url_rule('/post_event', view_func=add_event_route, methods=['POST'])
app.add_url_rule('/event/<int:event_id>', view_func=lambda event_id: event_show(event_id), endpoint='lambda1')
with app.app_context():
    app.add_url_rule('/evnts_sort/<string:sort>', view_func=lambda sort: sorted_events(sort), endpoint='lambda3', methods=['GET'])



# URL для статических ресурсов
app.add_url_rule('/resources', view_func=resources)
app.add_url_rule('/extra', view_func=extra)

# URL для услуг
app.add_url_rule('/services', view_func=services)
app.add_url_rule('/add_service', view_func=add_service, methods=['GET', 'POST'])

# URL для форума
app.add_url_rule('/forum', view_func=forum)
app.add_url_rule('/forum/new', methods=['GET', 'POST'], view_func=new_topic)
app.add_url_rule('/forum/topic/<int:topic_id>', view_func=lambda topic_id: topic(topic_id), endpoint='lambda2', methods=['GET', 'POST'])

# URL для профиля
app.add_url_rule('/profile', view_func=profile)
app.add_url_rule('/red_profile', view_func=set_profile, methods=['GET', 'POST'])
app.add_url_rule('/update_profile', view_func=update_profile, methods=['GET', 'POST'])
app.add_url_rule('/upload_profile_image', view_func=upload_profile_image, methods=['POST'])
app.add_url_rule('/current_image', view_func=current_profile_image, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
    init_db(app)
