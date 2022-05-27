"""Module that connects to the threat_attachment table"""
from datetime import datetime
from app import db


class ThreatAttachment(db.Model):
    """Model that represents the threat_attachment table"""
    __tablename__ = 'threat_attachment'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(140), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'))
    extension_id = db.Column(db.Integer, db.ForeignKey('attachment_extension.id'))

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        attachment = ThreatAttachment(address="/address")
        attachment.save()
        return f'<Threat attachment {self.address}>'
