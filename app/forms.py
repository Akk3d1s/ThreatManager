import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, MultipleFileField, IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import NumberRange, ValidationError, DataRequired, Email, EqualTo
from app.models.user import User
from app import ALLOWED_EXTENSIONS
from flask_wtf.file import FileField, FileAllowed, FileRequired
import pyotp

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    totp = IntegerField('Generated OTP', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    secret = HiddenField('Secret', validators=[DataRequired()])
    totp = IntegerField('Generated OTP', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_password(self, password):
        """
            Verify the strength of 'password'
            A password is considered strong if:
                8 characters length or more
                1 digit or more
                1 symbol or more
                1 uppercase letter or more
                1 lowercase letter or more
            Original Source: https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions#32542964
        """

        # calculating the length
        length_error = len(password.data) < 8

        # searching for digits
        digit_error = re.search(r"\d", password.data) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password.data) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password.data) is None

        # searching for symbols
        symbol_error = re.search(r"\W", password.data) is None

        # overall result
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

        if not password_ok:
            raise ValidationError('Password should be at least 8 characters in length and contain at least 1 digit, 1 symbol, 1 uppercase letter and 1 lowercase letter')

    def validate_totp(self, totp):
        if not pyotp.TOTP(self.secret.data).verify(totp.data):
            raise ValidationError('Please enter valid TOTP code.')


class ThreatReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    reproduce_steps = StringField('Steps', validators=[DataRequired()])
    # files = MultipleFileField('Files', validators=[FileRequired(), FileAllowed(files, 'Image only!')])
    file = FileField('File')


class ThreatCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])