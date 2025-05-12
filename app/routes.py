# Package imports
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
# Imports for login functionality
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from pytz import timezone
import sqlalchemy
from wtforms import ValidationError

# Local Imports
from .forms import LoginForm, RegisterForm, CreateListingForm  # Forms for user input
from .models import User, Listing, Book, Comment  # Models for DB entities
from . import db  # Database instance import from `__init__.py`

from sqlalchemy.orm import joinedload # Efficiently get data for comments. 


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
    login_form = LoginForm()
 
    if login_form.validate_on_submit():
        # Attempt to retrieve user from the database
        user = User.query.filter_by(email=login_form.email.data.lower()).first()
 
        # If user exists AND password matches exactly
        if user and user.pwd == login_form.password.data:
            login_user(user)
            return redirect(url_for('main.profile'))
        else:
            # Show error message below password field
            login_form.password.errors.append('Invalid email or password.')
 
    return render_template('login.html', form=login_form)

@bp.route('/register/', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
 
    if reg_form.validate_on_submit():
        # Create new user
        user = User(
            email=reg_form.email.data.lower(),
            fname=reg_form.first_name.data,
            lname=reg_form.last_name.data,
            major=reg_form.major.data,
            pwd=reg_form.password.data
        )
 
        db.session.add(user)
        db.session.commit()
        flash('Account created! Redirecting to login...')
        return redirect(url_for('main.login'))
 
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

    Added try block for errors handling. 
    '''
    try:
        # Retrieve all listings with related data efficiently
        listings = db.session.query(Listing).options(
            joinedload(Listing.book),
            joinedload(Listing.User),
            joinedload(Listing.comments).joinedload(Comment.user)
        ).order_by(Listing.timestamp.desc()).all()
        
        return render_template('listings.html', listings=listings)
    
    except Exception as e:
        flash(f"An error occurred while loading listings: {str(e)}")
        return redirect(url_for('main.profile'))

@bp.route('/listing/<int:listing_id>/comment', methods=['POST'])
@login_required
def add_comment(listing_id):
    '''
    Route to add a new comment to a specific listing.
    
    Args:
        listing_id (int): The ID of the listing to comment on
        
    Returns:
        Redirects to the listings page after comment submission
        
    Note:
        - Requires user authentication
        - Handles empty comments and database errors
        - Automatically timestamps comments
    '''
    try:
        content = request.form.get('comment')
        if not content:
            flash('Comment cannot be empty')
            return redirect(url_for('main.view_listings'))
            
        listing = Listing.query.get_or_404(listing_id)
        new_comment = Comment(
            text=content,
            userID=current_user.userID,
            listingID=listing_id,
            timeStamp=datetime.now(timezone('US/Eastern'))
        )
        
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully!")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding comment: {str(e)}")
    
    return redirect(url_for('main.view_listings'))



# ORLANDO
@bp.route('/logout')
@login_required  # Only logged-in users should be able to log out
def logout():
    '''
    Route triggered when user logs out of the application.
    '''
    logout_user()  # End the user's session
    flash("You have been logged out.")  # Optional message shown on next page
    # Send them back to the welcome page
    return redirect(url_for('main.welcome'))
