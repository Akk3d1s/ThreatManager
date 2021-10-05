from datetime import datetime
from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)