from datetime import datetime
from app import db

class ActionLog(db.Model):
    __tablename__ = 'action_log'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(64))
    action = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'user_id: {} action: {} '.format(self.user_id, self.action)

class ErrorLog(db.Model):
    __tablename__ = 'error_log'
    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(64))
    error = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'user_id: {} error: {} '.format(self.user_id, self.error)