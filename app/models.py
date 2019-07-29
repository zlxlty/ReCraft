from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime, timedelta
import random
import secrets
from .video_cover import get_cover
import os

class PictureSet(db.Model):
    __tablename__ = 'picturesets'

    id = db.Column(db.Integer, primary_key=True)
    dirname = db.Column(db.String(64), index=True, unique=True)
    prediction = db.Column(db.String(1024))

    def __repr__(self):
        return '<PictureSet %r>' % self.dirname

class Video(db.Model):
    __tablename__ = 'videos'
    __searchable__ = ['title','materials']
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    cover = db.Column(db.String(64))
    dirname = db.Column(db.String(64))
    materials = db.Column(db.String(256), index=True)

    @staticmethod
    def load_video():
        current_path = os.path.dirname(__file__)
        abs_path = os.path.join(current_path, 'static/video')
        file_names = os.listdir(str(abs_path))
        for name in file_names:
            path = os.path.join(abs_path, name)
            cover = get_cover(path)
            lables = name.split('.')[0].split('-')
            for i in range(len(lables)):
                for j in range(10):
                    lables[i] = lables[i].replace(str(j), '')
            v = Video(title=str(secrets.token_hex(4)), cover=cover, dirname=name, materials=str(lables))
            db.session.add(v)
        db.session.commit()

    def __repr__(self):
        return '<Video %r>' % self.title
