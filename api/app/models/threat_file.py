from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import backref, relationship
from app import db

@dataclass
class ThreatFile(db.Model):
    __tablename__ = 'file_threat'
    id: int
    file: str

    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(64))
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'), default=0)