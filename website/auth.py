from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST': # accepts the form if it POST method 
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  #checking if any user has the email which is received from the post method .first() returns the first user
        if user:
            if check_password_hash(user.password, password): #if user exists check wheather the passwords are same 
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error') #if the user doesn't exists returns the error 

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout(): #logging out 
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  # accepts the form if it POST method 
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()   #checking if any user has the email which is received from the post method .first() returns the first user
        if user:
            flash('Email already exists.', category='error')  #if the user exists already then it flashes any error 
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error') # checking validity of the password and email 
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256')) 
            db.session.add(new_user)# if the conditions match then the user is added to the database 
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
