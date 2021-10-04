from datetime import datetime
from app import db


class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(140))
    reproduce_steps = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('threat_status.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('threat_category.id'))
    # attachment_id = db.Column(db.Integer, db.ForeignKey('threat_attachment.id'))

    def __repr__(self):
        return '<Threat {}>'.format(self.title)