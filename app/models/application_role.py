"""Module that connects to the role_application table"""
from datetime import datetime
from app import db


class RoleApplication(db.Model):
    """Model that represents the role_application_table"""
    __tablename__ = 'role_application'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Role Application userId: {self.user_id}, roleId: {self.role_id}>'
