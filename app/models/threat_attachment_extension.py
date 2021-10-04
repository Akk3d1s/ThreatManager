from datetime import datetime
from app import db, login

class ThreatAttachmentExtension(db.Model):
    __tablename__ = 'attachment_extension'
    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Attachment extension {}>'.format(self.extension)
