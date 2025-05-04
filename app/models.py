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

    def get_id(self):
        '''
        Retrieves the user's ID when logging in to the
        application.
        '''
        return str(self.userID)
    

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
    threadID = db.Column(db.Integer, db.ForeignKey('Thread.threadID'))
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'))
    text = db.Column(db.String(500), nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)


class Book(db.Model):
    pass

class Thread(db.Model):
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
