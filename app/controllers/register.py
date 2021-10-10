from flask import render_template, flash, redirect, url_for
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from app import app, mail
from app.forms import RegistrationForm
from flask_login import current_user
from app.models.user import User

urlSafeTimedSerializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
maxConfirmationWaitingTime = 86400  # 24 hours


# todo - user model should be adjusted as the user can only be active, once email was confirmed

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, surname=form.surname.data, email=form.email.data, role_id=1)
        user.set_password(form.password.data)
        handle_registration_submission(user)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/confirm_account/<token>')
def confirm_account(token):
    # Here we should activate the user in the DB
    try:
        email = urlSafeTimedSerializer.loads(token, max_age=maxConfirmationWaitingTime)
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid request')
        else:
            user.is_active = True
            user.save()
            flash('Congratulations, your account is now active!')
    except SignatureExpired:
        flash('URL expired, please request another confirmation email.')
    except BadSignature:
        flash('URL is invalid, please contact support')
    return redirect(url_for('login'))


def handle_registration_submission(user):
    user.save()
    send_mail(user.email)


def send_mail(email):
    try:
        token = urlSafeTimedSerializer.dumps(email)
        confirmation_link = url_for('confirm_account', token=token, _external=True)
        message = Message('Account confirmation', sender='threatmanager@gmail.com', recipients=[email])
        message.body = 'Please confirm your account by copy and pasting this url: {}'.format(confirmation_link)
        mail.send(message)
        flash('A confirmation email has been sent to the provided email address. This url will only be valid for 24 '
              'hours')
    except:
        flash('Unable to send email, please contact support.')
