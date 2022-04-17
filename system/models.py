from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    contact = db.Column(db.String(10))
    hashCode = db.Column(db.String(120)) #for email verification during forgot password

class Contact(db.Model):
    id =  db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    name = db.Column(db.String(100))
    subject = db.Column(db.String(1000))
    message = db.Column(db.String(10000))

# class UserLog(db.Model):
#     id = db.Column(db.Integer, primary_key=True) 
#     userid = db.Column(db.Integer,db.ForeignKey(User.id))
#     function = db.Column(db.String(100))
#     timestamp = db.Column(db.String(100))

