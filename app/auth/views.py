from flask import flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from ..models import User
from .forms import LoginForm, RegisterForm
from .. import db

# Create a blueprint - make sure all BPs have unique names
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        first_name = register_form.first_name.data
        surname = register_form.surname.data
        email = register_form.email.data
        user = db.session.scalar(db.select(User).where(User.email==email))
        if user:
            flash('Email already exists, please try another')
            return redirect(url_for('auth.register'))
        password = register_form.password.data
        pwd_hash = generate_password_hash(password)
        phone = register_form.phone.data
        address = register_form.address.data
        new_user = User(first_name=first_name, surname=surname, email=email, password_hash=pwd_hash, phone=phone, address=address)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        return render_template('user.html', form=register_form)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email==email))
        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error, 'warning')
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))