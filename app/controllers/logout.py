"""
Contains a function handling a user logging out.
"""
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models.user import User
from werkzeug.urls import url_parse

@app.route('/logout')
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except Exception as error:
        print(error)