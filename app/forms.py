from flask_wtf import FlaskForm  # For form creation
# Fields for forms
from wtforms import StringField, DecimalField, SubmitField,\
     PasswordField, TextAreaField, DateTimeField
# Validation mechanisms
from wtforms.validators import DataRequired, Length, Email, ValidationError, Length
import datetime


class LoginForm(FlaskForm):
    '''
    Login form - used to allow a user to login with entered credentials.
    '''
    email = StringField('SCSU Email Address', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class RegisterForm(FlaskForm):
    """ 
    Registration form - takes input information from a User, creates an account
    for the user and writes the User's account to the database.
     """
    email = StringField('E-mail', validators=[
        DataRequired(), Email(), Length(min=4)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    password = PasswordField('Create password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_email(self, field):
        """
        Ensure the email ends with '@southernct.edu'
        """
        if not field.data.lower().endswith('@southernct.edu'):
            raise ValidationError('E-mail must be a Southern CT address')


class CreateListingForm(FlaskForm):
    '''
    Form responsible for creating a listing for a book.
    '''
    bookTitle = StringField('Book Title', validators=[
        DataRequired(), Length(max=100)
    ])

    author = StringField('Author', validators=[
        DataRequired(), Length(max=100)
    ])

    isbn = StringField('ISBN (only numbers)', validators=[
        DataRequired(), Length(min=13, max=13)
    ])

    subject = StringField('Subject', validators=[
        DataRequired(), Length(max=100)
    ])

    condition = StringField('Condition', validators=[
        DataRequired(), Length(max=100)
    ])

    listPrice = DecimalField('Asking Price ($)', validators=[
        DataRequired()
    ])

    origPrice = DecimalField('Original Purchased Price ($)', validators=[
        DataRequired()
    ])

    notes = TextAreaField('Notes (highlighted, dog-eared, etc)', validators=[
        DataRequired()
    ])

    timeStamp = DateTimeField(
        label='Post Time',
        format='%b %d %Y',
        render_kw={'readonly': True}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.timeStamp.data:
            self.timeStamp.data = datetime.date.today()

    submit = SubmitField('PUBLISH')
