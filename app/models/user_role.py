"""Module that connects to the user_role table"""
from datetime import datetime
from app import db
from enum import Enum


class UserRoles(Enum):
    """User role enums"""
    PUBLIC = 'PUBLIC'
    READ = 'READ'
    EDITOR = 'EDITOR'
    APPROVER = 'APPROVER'
    DEVELOPER = 'DEVELOPER'
    ADMIN = 'ADMIN'


class UserRole(db.Model):
    """Model that represents the user_role table"""
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), default=UserRoles.PUBLIC)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # role = UserRole(role='PUBLIC')
        # role.save()
        return f'<User Role {self.role}>'
