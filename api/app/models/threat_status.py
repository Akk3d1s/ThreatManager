'''ThreatStatus'''
from dataclasses import dataclass
from app import db

@dataclass
class ThreatStatus(db.Model):
    '''ThreatStatus model'''
    __tablename__ = 'threat_status'
    status: str

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default='PENDING')
