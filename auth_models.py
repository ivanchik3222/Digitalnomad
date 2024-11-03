# auth_models.py
from flask_login import UserMixin

class User(UserMixin):
    """User model for Flask-Login."""
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

if __name__ == '__main__':
    print("nuh uh")
else:
    print("import auth_models")