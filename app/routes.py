# Package imports
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
# Imports for login functionality
from flask_login import login_user, logout_user, login_required, current_user

# Local Imports
from .forms import LoginForm, RegisterForm, CreateListingForm  # Forms for user input
from .models import User, Listing, Book  # Models for DB entities
from . import db  # Database instance import from `__init__.py`


# Testing 
from sqlalchemy.orm import joinedload
from .models import Comment


bp = Blueprint("main", __name__)


@bp.route('/')
def welcome():
    '''
    Homepage route: The first page the user is
    presented with - at the root of the application.
    '''
    return render_template("welcome.html")


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    '''
    Login route - permitting user to enter their
    (valid) credentials to login to their account.
    '''
    # Initialize login form
    login_form = LoginForm()

    # Check if form was submitted
    if login_form.validate_on_submit():

        # Attempt to retrieve exisiting user from the database - from input email
        user = User.query.filter_by(email=login_form.email.data).first()

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
    '''
    Register a new user to the application.
    '''
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

    # Render the `register.html` template
    return render_template('register.html', form=reg_form)


@bp.route('/profile/')
@login_required
def profile():
    '''
    Route to the current user's profile page.
    '''
    # Pass current user instance to the profile template
    return render_template('profile.html', user=current_user)


# ORLANDO/Justin
# Create listing route for the user to post a listing
@bp.route('/create_listing', methods=['GET', 'POST'])
def create_listing():
    '''
    Route presenting form to create a new listing
    with associated book
    '''
    # Create a new instance of the CreateListingForm
    list_form = CreateListingForm()
    # If the form is submitted and the data is valid
    if list_form.validate_on_submit():

        # Initialize the book using the form inputs
        book = Book(bookTitle=list_form.bookTitle.data, origPrice=list_form.origPrice.data, listPrice=list_form.listPrice.data,
                    isbn=list_form.isbn.data, condition=list_form.condition.data, notes=list_form.notes.data, author=list_form.author.data,
                    subject=list_form.subject.data, userID=session['_user_id'])

        # Initialize the listing
        listing = Listing(book=book, timestamp=list_form.timeStamp.data,
                          userID=session['_user_id'])

        # Add both book and listing to the database session
        db.session.add(book)
        db.session.add(listing)
        db.session.commit()  # Write permanently to the DB

        flash("Listing submitted!")
        return redirect(url_for('main.view_listings'))

    # Show the create_listing page with the form
    return render_template('create_listing.html', form=list_form)


# TATIANA
# Route to view listings
@bp.route('/listings')
def view_listings():
    '''
    Route displaying ALL active listings.
    '''

    # Retrieve all listings from the DB
    # listings = db.session.query(Listing).all()

    listings = db.session.query(Listing).options(
            joinedload(Listing.comment).joinedload(
                        Comment.user)).all()

    # Pass the listings to the template
    return render_template('listings.html', listings=listings)


@bp.route('/listings/<int:listing_id>/comment', methods=['POST'])
@login_required
def add_comment(listing_id):
    content = request.form.get('comment')
    new_comment = Comment(content=content, user_id=current_user.id, listingID=listing_id)
    db.session.add('new_comment')
    db.session.commit()
    flash("Comment added!")
    return redirect(url_for('main.view_listings'))



# ORLANDO
@bp.route('/logout')
@login_required  # Only logged-in users should be able to log out
def logout():
    '''
    Route triggered when user logs out of the application.
    '''
    logout_user()  # End the user’s session
    flash("You have been logged out.")  # Optional message shown on next page
    # Send them back to the welcome page
    return redirect(url_for('main.welcome'))
