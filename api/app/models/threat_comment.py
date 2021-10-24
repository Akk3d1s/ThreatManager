'''ThreatComment'''
from dataclasses import dataclass
from datetime import datetime
from app import db

@dataclass
class ThreatComment(db.Model):
    '''ThreatComment model'''
    __tablename__ = 'comment'
    comment: str
    created_at: str
    user_id: int

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0)
