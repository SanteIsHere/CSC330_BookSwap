from . import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = 'User'

    userID = db.Column(db.Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pwd = db.Column(db.String(50), nullable=False)

    # Establish relationship between 'User' and 'Book' tables
    books = db.relationship('Book', backref='User')

    # Establish relationship between 'User' and 'Listing' tables
    listings = db.relationship('Listing', backref='User')



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
    origPrice = db.Column(db.Numeric(10, 2), nullable=False)
    listPrice = db.Column(db.Numeric(10, 2), nullable=False)
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

    # Tie comments to a listing
    comments = db.relationship('Comment', backref='Listing', lazy='select')

class Comment(db.Model):
    __tablename__ = 'Comment'

    commentID = db.Column(db.Integer, primary_key=True,
                          nullable=False, autoincrement=True)
    listingID = db.Column(db.Integer, db.ForeignKey('Listing.listingID'))
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    text = db.Column(db.String(500), nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)

    # Tie listing to a comment
    user = db.relationship('User', backref='comments')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
