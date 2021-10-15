from datetime import datetime
from app import db

class ThreatFile(db.Model):
    __tablename__ = 'file_threat'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(64))
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Threat File Name {}'.format(self.file)

class CommentFile(db.Model):
    __tablename__ = 'file_comment'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(64))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Comment File Name {}'.format(self.file)

