from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from .models import User
from . import db

bp = Blueprint("main", __name__)


@bp.route('/')
def welcome():
    return render_template("welcome.html")


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    # Initialize login form
    login_form = LoginForm()

    # Check if form was submitted
    if login_form.validate_on_submit():

        # Retrieve user from the database
        user = User.query.filter_by(email=login_form.email)

        if user:
            # If the user is successfully retrieved, log them in
            login_user(user)
            # And redirect to homepage
            return redirect(url_for('main.welcome'))
        else:
            # User not found
            flash('Invalid username or password. Try again.')

    # Render the `login.html` template
    return render_template('login.html', form=login_form)


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    # Initialize registration form
    reg_form = RegisterForm()

    # Check if form was submitted and input data is validated
    if reg_form.validate_on_submit():

        # Create new user with form input
        user = User(email=reg_form.email, fname=reg_form.first_name,
                    lname=reg_form.last_name, major=reg_form.major,
                    pwd=reg_form.password)

        # Add new user to database
        db.session.add(user)
        db.session.commit()
        flash('Account Created! Redirecting to profile...')
        return redirect(url_for('main.profile'))

    # Render the `register.html` template
    return render_template('register.html', form=reg_form)


@bp.route('/profile/')
def profile():
    return render_template('profile.html')


@bp.route('/listings')
def listings_view():
    # TODO: Implement this route
    pass


@bp.route('/create_listing')
def create_listing():
    # TODO: Implement this route
    pass

# TODO: Implement logout route and functionality
