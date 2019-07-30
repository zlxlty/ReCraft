from flask_migrate import Migrate, upgrade
from dotenv import load_dotenv
from app import create_app, db
from app.models import Video, PictureSet, User, Comment
import os
from random import randint

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Video=Video, PictureSet=PictureSet, User=User, Comment=Comment)

@app.cli.command()
def deploy():
    '''Run deployment tasks'''
    upgrade()
    Video.load_video()
    for v in Video.query.all():
        v.difficulties = randint(0,2)
    db.session.commit()