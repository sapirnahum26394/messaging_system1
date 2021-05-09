from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Text)
    receiver = db.Column(db.Text)
    message = db.Column(db.Text)
    subject = db.Column(db.Text)
    date = db.Column(db.Text)
    opened = db.Column(db.Boolean, default=False)
