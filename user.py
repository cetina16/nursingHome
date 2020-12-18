from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, password,name):
        self.email = email
        self.password = password
        self.name = name
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    password = current_app.config["PASSWORDS"].get(user_id)
    name = current_app.config["USER_NAMES"].get(user_id)
    user = User(user_id, password,name) if password else None
    if user is not None:
        user.is_admin = user.email in current_app.config["USERS"]
    return user