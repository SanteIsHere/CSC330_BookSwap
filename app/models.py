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

    userID = db.Column(db.Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pwd = db.Column(db.String(50), nullable=False)

# TATIANA


class Listing(db.Model):
    """
    Represents a textbook listing posted by a user.
    """
    __tablename__ = 'Listing'

    listingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)
    comments = db.Column(db.String(500), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.userID'), nullable=False)
    user = db.relationship('User', backref='listings')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
