from datetime import datetime
from app import db
from enum import Enum

class Roles(Enum):
    PUBLIC = 'PUBLIC'
    READ = 'READ'
    EDITOR = 'EDITOR'
    APPROVER = 'APPROVER'
    DEVELOPER = 'DEVELOPER'
    ADMIN = 'ADMIN'

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