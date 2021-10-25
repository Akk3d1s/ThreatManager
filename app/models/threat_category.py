from datetime import datetime
from app import db
from enum import Enum

class ThreatCategories(Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

class ThreatCategory(db.Model):
    __tablename__ = 'threat_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), default=ThreatCategories.MEDIUM)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        category = ThreatCategory(category='MEDIUM')
        category.save()
        return '<Threat Category {}>'.format(self.category)