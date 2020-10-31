from functools import wraps

from flask_login import UserMixin, AnonymousUserMixin, current_user
from werkzeug.exceptions import abort


def man_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_manager:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


class User(UserMixin):
    def __init__(self, user_id, email, name, surname, pwd, is_manager, balance):
        self.id = user_id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.is_manager = is_manager
        self.balance = balance


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = None
        self.is_manager = False


class Projection:
    def __init__(self, proj_id, proj_date, proj_time, room, price, tickets_left):
        self.id = proj_id
        self.date = proj_date
        self.time = proj_time
        self.room = room
        self.price = price
        self.tickets_left = tickets_left
