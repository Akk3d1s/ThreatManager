'''UserRole'''
from app import db

class UserRole(db.Model):
    '''UserRole model'''
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), default='PUBLIC')
