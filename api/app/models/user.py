from app import db
from werkzeug.security import check_password_hash
from dataclasses import dataclass
from sqlalchemy.orm import backref, relationship


@dataclass
class User(db.Model):
    id: int
    email: str
    password: str
    is_active: bool
    role: str

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'))
    role = relationship('UserRole', backref='user')

    def check_password(self, password):
        return check_password_hash(self.password, password)
