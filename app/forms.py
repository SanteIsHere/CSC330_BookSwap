from flask_wtf import FlaskForm  # For form creation
# Fields for forms
from wtforms import StringField, PasswordField, SubmitField
# Validation mechanisms
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('SCSU Email Address', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(), Length(min=4)])
    full_name = StringField('Full Name', validators=[DataRequired()])
    password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
