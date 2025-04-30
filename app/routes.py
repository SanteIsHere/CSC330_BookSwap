from flask import Blueprint, render_template, redirect, url_for
from .forms import LoginForm, RegisterForm

bp = Blueprint("main", __name__)


@bp.route('/')
def welcome():
    return render_template("welcome.html")


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    # Initialize login form
    login_form = LoginForm()

    # Render the `login.html` template
    return render_template('login.html', form=login_form)


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    # Initialize registration form
    registration_form = RegisterForm()

    # Render the `register.html` template
    return render_template('register.html', form=registration_form)


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
