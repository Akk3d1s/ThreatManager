from flask import render_template, flash, redirect, url_for, request, Markup, session
from app import app, url_safe_timed_serializer
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models.user import User
from werkzeug.urls import url_parse
import pyotp
import time


@app.route('/login', methods=['GET', 'POST'])
def login():
    max_allowed_login_attempts = 5
    # Redirect user if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # Handle form submission (POST requests)
    if form.validate_on_submit():
        if session['login_attempts'] >= max_allowed_login_attempts:
            if time.time() - session['last_login'] < 3600:
                flash('Max login attempts reached. Try again in 1 hour.')
                return redirect(url_for('login'))
            else:
                reset_failed_login()
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data) or not pyotp.TOTP(user.totp_secret).verify(form.totp.data):
            record_failed_login()
            flash('Invalid email, password or TOTP code. ' + str(max_allowed_login_attempts - session['login_attempts']) + ' attempts left')
            return redirect(url_for('login'))
        elif not user.is_active:
            record_failed_login()
            token = url_safe_timed_serializer.dumps(user.email)
            flash(Markup('Please confirm account. Click <a href="/resend_confirmation/' + token + '">here</a> to '
                                                                                                'resend '
                                                                                                'confirmation '
                                                                                                'email.'))
            return redirect(url_for('login'))
        reset_failed_login()
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

def record_failed_login():
    session['last_login'] = time.time()
    session['login_attempts'] += 1

def reset_failed_login():
    session['login_attempts'] = 0
