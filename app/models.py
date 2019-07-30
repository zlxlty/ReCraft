from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime, timedelta
import random
import secrets
from flask_login import UserMixin
from .video_cover import get_cover
import os

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

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
    difficulties = db.Column(db.Integer, index=True)

    def get_materials(self):
        res = ''
        materials = eval(self.materials)
        for material in materials:
            res += (str(material)+', ')

        return res

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
