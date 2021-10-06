from datetime import datetime
from app import db

class RoleApplication(db.Model):
    __tablename__ = 'role_application'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))

    def __repr__(self):
        return '<Role Application userId: {}, roleId: {}>'.format(self.user_id, self.role_id)