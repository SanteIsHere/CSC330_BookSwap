from . import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """
    User object to represent a user in the system.

    Attributes: 
        first_name (str): String of the users first name.
        last_name (str): String of the users last name.
        major (str): String of the user's major.
        email (str): String of the user's email.
        pwd (str): String of the user's password.

    """
    __tablename__ = 'User'

    userID = db.Column(db.Integer(), primary_key=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(50), nullable=False)

    def __init__(self, fname, lname, major, email, pwd):
        self.first_name = fname
        self.last_name = lname
        self.major = major
        self.email = email
        self.pwd = pwd


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
