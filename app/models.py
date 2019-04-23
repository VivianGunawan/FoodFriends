from app import db
from datetime import datetime

class User(db.Model):
    facebook_id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.Text,index=True, unique=True)
    location = db.Column(db.Text,index=True, unique=False)
    friends =db.Column(db.Text,index=True, unique=False)
    meals = db.relationship('Meal', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.facebook_id'))

    def __repr__(self):
        return '<Meal {}>'.format(self.body)
