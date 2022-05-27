"""Module that connects to the attachment_extension table"""
from app import db

class ThreatAttachmentExtension(db.Model):
    """Model that represents the attachment_extension table"""
    __tablename__ = 'attachment_extension'
    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f'<Attachment extension {self.extension}>'
