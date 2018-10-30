from flask import render_template
from flask_login import login_required
from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from . import admin
from main import db
from main import UserWeb
from form import LoginForm


@admin.route('/')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pengguna = UserWeb.query.filter_by(username = form.username.data).first()
        if pengguna is not None adn pengguna.verify_password(
        form.password.data
        ):
        login_user(pengguna)
        return redirect(url_for('admin.dashboard'))

        else:
            flash('invalid username and password')
    return render_template('admin/index.html', form = form, title = 'Login')

@admin.route('/wri/admin/dashboard/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html', title = "Wri Dashboard")

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('#'))
