from flask_login import UserMixin, AnonymousUserMixin


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


class InsufficientBalanceException(Exception):
    def __init__(self, balance, message="Insufficient funds"):
        self.balance = balance
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.balance} -> {self.message}'


class TimeNotAvailableException(Exception):
    def __init__(self, datetime, message="Projection overlaps current schedule"):
        self.datetime = datetime
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.datetime} -> {self.message}'
