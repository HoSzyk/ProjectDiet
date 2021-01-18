from flask import Flask, render_template
from dietapp import app
import copy
import random
import secrets
import os
from flask import render_template, flash, redirect, url_for, request, json
from sqlalchemy import or_, and_, func
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from dietapp.forms import *
from dietapp.models import *
import datetime


# Main view
@app.route('/')
@app.route('/home')
@login_required
def home():
    enabled_tabs = create_enabled_tabs()
    enabled_tabs['product'] = False
    return render_template('products.html', title='Produkty', enabled_tabs=enabled_tabs, products=[{
        'name': 'test',
        'information': 'test test'
    }])


# Login view
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Instance of LoginForm
    form = LoginForm()
    # Check that HTTP request is POST and form is valid
    if request.method == 'POST' and form.validate():
        # Check if user exists in database
        user = User.query.filter_by(email=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nazwa użytkownika lub hasło jest niepoprawne', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form, title='Logowanie')


@app.route("/register/", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Instance of RegisterForm
    form = RegisterForm()

    # Check that HTTP request is POST and form is valid
    if request.method == 'POST' and form.validate_on_submit():
        # Generate hashed password for database
        password_hashed = generate_password_hash(form.password.data, method='sha256')

        # Model object
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=password_hashed
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Zarejestrowano pomyślnie!", 'success')
        # Redirect to login page
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form=form, title='Rejestracja')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def create_enabled_tabs():
    return {
        'product':  True,
        'diet': True,
        'meal': True,
        'stats': True
    }
