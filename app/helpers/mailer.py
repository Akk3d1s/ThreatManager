from flask_mail import Message
from app import mail
from flask import flash, url_for


class Mailer:
    @staticmethod
    def send_confirmation_mail(email, token):
        try:
            confirmation_link = url_for('confirm_account', token=token, _external=True)
            message = Message('Account confirmation', sender='threatmanager@gmail.com', recipients=[email])
            message.body = 'Please confirm your account by copy and pasting this url: {}'.format(confirmation_link)
            mail.send(message)
            flash(
                'A confirmation email has been sent to the provided email address. This url will only be valid for 24 '
                'hours')
        except:
            flash('Unable to send email, please contact support.')