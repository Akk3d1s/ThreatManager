"""Module that connects to the theat_status table"""
from datetime import datetime
from app import db
from enum import Enum


class ThreatStatuses(Enum):
    """Different Threat status enums"""
    PENDING = 'PENDING'
    APPROVINGNEWCASE = 'APPROVINGNEWCASE'
    RESOLVING = 'RESOLVING'
    APPROVINGENDCASE = 'APPROVINGENDCASE'
    RESOLVED = 'RESOLVED'
    REJECTED = 'REJECTED'
    CANCELED = 'CANCELED'


class ThreatStatus(db.Model):
    """Model that represents the threat_status table"""
    __tablename__ = 'threat_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64), default=ThreatStatuses.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        status = ThreatStatus(status='PENDING')
        status.save()
        return f'<Threat Status {self.status}>'
