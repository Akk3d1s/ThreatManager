from datetime import datetime
from app import db

class File(db.Model):
    pass
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(64))
    threat_id = db.Column(db.Integer, db.ForeignKey('threat.id'), default=0)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'File Address {}'.format(self.address)
