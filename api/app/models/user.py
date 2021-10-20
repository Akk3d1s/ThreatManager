from app import db
from werkzeug.security import check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        return check_password_hash(self.password, password)
