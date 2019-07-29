from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime, timedelta
import random
import secrets

class PictureSet(db.Model):
    __tablename__ = 'picturesets'

    id = db.Column(db.Integer, primary_key=True)
    dirname = db.Column(db.String(64), index=True, unique=True)
    prediction = db.Column(db.String(1024))

    def __repr__(self):
        return '<PictureSet %r>' % self.dirname

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    dirname = db.Column(db.String(64), index=True)
    materials = db.Column(db.String(256), index=True)

    def __repr__(self):
        return '<Video %r>' % self.title
# class Moment(db.Model):
#     __tablename__ = 'moments'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     pictures = db.Column(db.String(128), nullable=False)
