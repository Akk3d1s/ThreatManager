from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from enum import Enum

class Roles(Enum):
    PUBLIC = 'PUBLIC'
    READ = 'READ'
    EDITOR = 'EDITOR'
    APPROVER = 'APPROVER'
    DEVELOPER = 'DEVELOPER'
    ADMIN = 'ADMIN'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(64), nullable=True)
    surname = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    threats = db.relationship('Threat', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Threat {}>'.format(self.body)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), default=Roles.PUBLIC)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        role = Role(role='PUBLIC')
        role.save()
        return '<Role {}>'.format(self.role)
