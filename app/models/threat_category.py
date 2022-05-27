"""Module that connects to the threat_category table"""
from datetime import datetime
from enum import Enum
from app import db


class ThreatCategories(Enum):
    """Threat category enums"""
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'


class ThreatCategory(db.Model):
    """Model that represents the comment table"""
    __tablename__ = 'threat_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), default=ThreatCategories.MEDIUM)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        category = ThreatCategory(category='MEDIUM')
        category.save()
        return f'<Threat Category {self.category}>'
