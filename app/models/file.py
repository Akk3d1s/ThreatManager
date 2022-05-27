"""Module that connects to the file_threat and file_comment table"""
from datetime import datetime
from app import db


class ThreatFile(db.Model):
    """Model that represents the file_threat table"""
    __tablename__ = 'file_threat'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(64))
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Threat File Name {self.file}'


class CommentFile(db.Model):
    """Model that represents the file_comment table"""
    __tablename__ = 'file_comment'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(64))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        """Persist the model data"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Comment File Name {self.file}'
