from flask import Blueprint, render_template, redirect, url_for
from .forms import LoginForm, RegisterForm

bp = Blueprint("main", __name__)


@bp.route('/')
def welcome():
    return render_template("welcome.html")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Initialize login form
    login_form = LoginForm()

    return render_template('login.html', form=login_form)
