from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, CreateListingForm
from .models import User, Listing
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

        # Attempt to retrieve user from the database - from input email
        user = User.query.filter_by(email=login_form.email.data).first()

        # # DEBUG
        # print("User found: ", user)

        if user:
            # If the user is successfully retrieved, log them in
            login_user(user)
            # And redirect to homepage
            return redirect(url_for('main.profile'))
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
        user = User(email=reg_form.email.data, fname=reg_form.first_name.data,
                    lname=reg_form.last_name.data, major=reg_form.major.data,
                    pwd=reg_form.password.data)

        # Add new user to database
        db.session.add(user)
        db.session.commit()
        flash('Account Created! Redirecting to login page...')
        # Redirect the user to the login page
        return redirect(url_for('main.login'))

    # # DEBUG
    # print("Form submitted: ", reg_form.validate_on_submit())
    # print("Errors:", reg_form.errors)

    # Render the `register.html` template
    return render_template('register.html', form=reg_form)


@bp.route('/profile/')
@login_required
def profile():
    # Pass current user instance to the profile template
    return render_template('profile.html', user=current_user)


# ORLANDO
# Create listing route for the user to post a listing
@bp.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    # Create a new instance of the CreateListingForm
    form = CreateListingForm()

    # If the form is submitted and the data is valid
    if form.validate_on_submit():
        # Right now we’re not saving to the database yet
        # Just showing a success message so we can test the form
        flash("Listing submitted! (Not yet saved to the database)")
        return redirect(url_for('main.listings_view'))

    # Show the create_listing page with the form
    return render_template('create_listing.html', form=form)


# TATIANA
# Route to view listings
@bp.route('/listings')
def view_listings():
    # Simulated listings (mock data)
    dummy_listings = [
        {
            "title": "Algebra 2",
            "author": "Cormen et al.",
            "course": "MAT 120",
            "price": 45.00,
            "image_filename": "dummy_book_1.jpg",
            "comments": "Some highlighting, good condition.",
            "user_fname": "Alice",
            "user_lname": "Johnson"
        },
        {
            "title": "Organic Chemistry",
            "author": "Axler",
            "course": "CHE 260",
            "price": 35.00,
            "image_filename": "dummy_book_2.jpg",
            "comments": "",
            "user_fname": "Bob",
            "user_lname": "Lee"
        }
    ]

    return render_template('listings.html', listings=dummy_listings)

# ORLANDO
# Route to log the user out


@bp.route('/logout')
@login_required  # Only logged-in users should be able to log out
def logout():
    logout_user()  # End the user’s session
    flash("You have been logged out.")  # Optional message shown on next page
    # Send them back to the welcome page
    return redirect(url_for('main.welcome'))
