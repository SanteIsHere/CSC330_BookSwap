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

    # Establish relationship between 'User' and 'Book' tables
    user_book = db.relationship('Book', backref='User')

    # Establish relationship between 'User' and 'Listing' tables
    user_listing = db.relationship('Listing', backref='User')

    def get_id(self):
        '''
        Retrieves the user's ID when logging in to the
        application.
        '''
        return str(self.userID)


class Book(db.Model):

    __tablename__ = 'Book'

    bookID = db.Column(db.Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    bookTitle = db.Column(db.String(50), nullable=False)
    origPrice = db.Column(db.Float, nullable=False)
    listPrice = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    isbn = db.Column(db.Integer, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(50), nullable=True)


class Listing(db.Model):

    __tablename__ = "Listing"

    listingID = db.Column(db.Integer, primary_key=True,
                          nullable=False, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    bookID = db.Column(db.Integer, db.ForeignKey('Book.bookID'))
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'))

    # Tie book to a listing
    book = db.relationship('Book', backref='Listing')


class Comment(db.Model):
    """
    Comment object to represent a comment in the system.

    Attributes:
        commentID (int): Integer of the comment ID. 
        threadID (int): Integer of the thread ID.
        userID (int): Integer of the user ID.
        text (str): String of the comment text.
        timeStamp (datetime): Date and time of the comment.

    """
    __tablename__ = 'Comment'

    commentID = db.Column(db.Integer, primary_key=True,
                          nullable=False, autoincrement=True)
    listingID = db.Column(db.Integer, db.ForeignKey('Listing.listingID'))
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    text = db.Column(db.String(500), nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
