"""Module to handle the sending of mail"""
from flask_mail import Message
from flask import flash, url_for
from app import mail


class Mailer:
    """Sends a confirmation of email address email to the user registering for an account"""
    @staticmethod
    def send_confirmation_mail(email, token):
        """Send confirmation mail"""
        try:
            confirmation_link = url_for('confirm_account', token=token, _external=True)
            message = Message(
                'Account confirmation',
                sender='threatmanager@gmail.com',
                recipients=[email])
            message.body = f'Please confirm your account by copy ' \
                           f'and pasting this url: {confirmation_link}'
            mail.send(message)
            flash(
                'A confirmation email has been sent to the provided email address. '
                'his url will only be valid for 24 hours')
        except ValueError as error:
            flash(f'Unable to send email, please contact support. {error}')
