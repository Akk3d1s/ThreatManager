'''ThreatCategory'''
from dataclasses import dataclass
from app import db


@dataclass
class ThreatCategory(db.Model):
    '''ThreatCategory model'''
    __tablename__ = 'threat_category'
    category: str

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), default='MEDIUM')
