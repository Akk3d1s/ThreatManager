from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    surename = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    threats = db.relationship('Threat', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.firstname+' '+self.surename)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), index=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.role)

class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(140))
    recreation_steps = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('threat_status.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('threat_category.id'))
    attachment_id = db.Column(db.Integer, db.ForeignKey('threat_attachment.id'))

    def __repr__(self):
        return '<Threat {}>'.format(self.title)

class ThreatStatus(db.Model):
    __tablename__ = 'threat_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Threat Status {}>'.format(self.status)

class ThreatCategory(db.Model):
    __tablename__ = 'threat_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Threat Category {}>'.format(self.category)

class ThreatAttachment(db.Model):
    __tablename__ = 'threat_attachment'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(140), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    extension_id = db.Column(db.Integer, db.ForeignKey('attachment_extension.id'))

    def __repr__(self):
        return '<Threat attachment {}>'.format(self.address)

class AttachmentExtension(db.Model):
    __tablename__ = 'attachment_extension'
    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Attachment extension {}>'.format(self.extension)



