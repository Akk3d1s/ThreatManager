from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import backref, relationship
from app import db


@dataclass
class Threat(db.Model):
    __tablename__ = 'threat'
    id: int
    title: str
    description: str
    reproduce_steps: str
    timestamp: str
    progress: str
    threat_level: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(140))
    reproduce_steps = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('threat_status.id'))
    progress = relationship('ThreatStatus', backref='threat')
    category_id = db.Column(db.Integer, db.ForeignKey('threat_category.id'))
    threat_level = relationship('ThreatCategory', backref='threat')