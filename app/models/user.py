"""Module that connects to the user table"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


@login.user_loader
def load_user(id):
    """Fetch user by id"""
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Model that represents the user table"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    totp_secret = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    threats = db.relationship('Threat', backref='author', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=False)

    def __repr__(self):
        user_full_name = self.first_name + ' ' + self.surname
        return f'<User {user_full_name}>'

    def set_password(self, password):
        """Update user password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check user password"""
        return check_password_hash(self.password, password)

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the model data"""
        db.session.delete(self)
        db.session.commit()
