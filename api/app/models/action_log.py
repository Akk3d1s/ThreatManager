'''Action log'''
from datetime import datetime
from app import db

class ActionLog(db.Model):
    '''Handle persisting action logs'''
    __tablename__ = 'action_log'

    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(64))
    action = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        '''Save log into db'''
        db.session.add(self)
        db.session.commit()
