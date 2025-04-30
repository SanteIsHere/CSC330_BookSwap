
from app import db

class User(db.Model): 
    """
    User object to represent a user in the system.

    Attributes: 
        name (str): User's full name.
        email (str): Email address of the user.
        major (str): Major of the user.
        role (str): Role of the user (student or admin).
        userID (str): Identifier of the user. 
        interests (list): Interests of user, stored in a list.
        favorites (list): List of favorite listings saved by the user.
    """
    __tablename__ = 'User'

    userID = db.column(db.Integer(), primary_key=True, nullable = False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(50), nullable=False)


    def __init__(self, fname,lname, major, userID):
        self._fname = fname
        self._lname = lname
        self._major = major
        self._userID = userID
        
    