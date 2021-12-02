from flask_login import UserMixin
from __init__ import db,postamail

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    contact = db.Column(db.String(10))
    hashCode = db.Column(db.String(120)) #for email verification during forgot password