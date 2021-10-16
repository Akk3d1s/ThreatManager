from flask import render_template, flash, redirect, url_for, Markup, request
import pyotp
from itsdangerous import SignatureExpired, BadSignature
from app import app, url_safe_timed_serializer, max_confirmation_waiting_time, max_confirmation_resend_waiting_time
from app.forms import RegistrationForm
from flask_login import current_user, login_user
from app.helpers.mailer import Mailer
from app.models.user import User


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    secret = pyotp.random_base32()
    form = RegistrationForm(secret=secret)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, surname=form.surname.data, email=form.email.data, role_id=1, totp_secret=form.secret.data)
        user.set_password(form.password.data)
        handle_registration_submission(user)
        flash('secret from form', form.secret.data)
    return render_template('register.html', title='Register', form=form, secret=form.secret.data)


@app.route('/confirm_account/<token>')
def confirm_account(token):
    # Activate the user if successful
    try:
        email = url_safe_timed_serializer.loads(token, max_age=max_confirmation_waiting_time)
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid request')
        elif user.is_active:
            flash('Account already activated. Please login')
        else:
            user.is_active = True
            user.save()
            flash('Congratulations, your account is now active!')
    except SignatureExpired:
        email = url_safe_timed_serializer.loads(token)
        new_token = url_safe_timed_serializer.dumps(email)
        flash(Markup('URL expired. Click <a href="/resend_confirmation/' + new_token + '">here</a> to '
                                                                                              'resend '
                                                                                              'confirmation '
                                                                                              'email.'))
    except BadSignature:
        flash('URL is invalid, please contact support')
    return redirect(url_for('login'))


@app.route('/resend_confirmation/<token>')
def resend_confirmation(token):
    try:
        email = url_safe_timed_serializer.loads(token, max_age=max_confirmation_resend_waiting_time)
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Link may have expired, please try to log in again')
        else:
            confirmation_token = url_safe_timed_serializer.dumps(email)
            Mailer.send_confirmation_mail(email, confirmation_token)
    except BadSignature:
        flash('Invalid request')
    return redirect(url_for('login'))


def handle_registration_submission(user):
    user.save()
    token = url_safe_timed_serializer.dumps(user.email)
    Mailer.send_confirmation_mail(user.email, token)
