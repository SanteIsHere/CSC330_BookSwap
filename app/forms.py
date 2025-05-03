from flask_wtf import FlaskForm  # For form creation
# Fields for forms
from wtforms import StringField, PasswordField, SubmitField
# Validation mechanisms
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError


class LoginForm(FlaskForm):
    email = StringField('SCSU Email Address', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class RegisterForm(FlaskForm):
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



from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileAllowed

class CreateListingForm(FlaskForm):
    title = StringField('Book Title', validators=[
        DataRequired(), Length(max=100)
    ])

    author = StringField('Author', validators=[
        DataRequired(), Length(max=100)
    ])

    course = StringField('Class Used For', validators=[
        DataRequired(), Length(max=100)
    ])

    image = FileField('Upload Book Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

    price = DecimalField('Asking Price ($)', validators=[
        DataRequired(), NumberRange(min=0)
    ])

    submit = SubmitField('PUBLISH')


