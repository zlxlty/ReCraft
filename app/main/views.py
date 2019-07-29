'''
@Description: View file for main blueprint
@Author: Tianyi Lu
@Date: 2019-07-05 17:27:28
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-30 04:18:55
'''
import os
import json
from flask import render_template, session, redirect, url_for, current_app, flash, request, Markup, abort
from .. import db
from . import main
from resnet152_transfer import res_transfer
from ..image_saver import saver
from datetime import datetime
from ..models import PictureSet

path1 = os.path.abspath('./app')

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        dt = datetime.utcnow()
        dt_string = dt.strftime("%Y-%m-%d-%H-%M-%S")

        pictures = request.files.getlist('pictures')
        for picture in pictures:
            saver(dt_string, picture)

        return redirect(url_for('main.imageset', dirname=dt_string))

        
    return render_template('index.html')

@main.route('/video/<int:id>')
def video(id):
    return render_template('video.html', filename=filename)

@main.route('/imageset/<dirname>', methods=['GET', 'POST'])
def imageset(dirname):
    print(dirname)
    path = os.path.join(current_app.root_path, current_app.config['IMG_PATH'])
    if not os.path.exists(path):
        abort(404)

    pictureset = PictureSet.query.filter_by(dirname=dirname).first()
    if not pictureset:
        predict = res_transfer.predict(path, dirname)
        predict = json.dumps(predict)
        pictureset = PictureSet(dirname=dirname, prediction=predict)
        db.session.add(pictureset)
        db.session.commit()
    
    predict = json.loads(pictureset.prediction)
        
    return render_template('imageset.html', dirname=dirname, predict=predict)

@main.route('/predict')
def predict():
    data_dir = os.path.join(path1, 'static/user_img/01')
    predict = res_transfer.predict(data_dir, '2019-07-29-01')
    return render_template('predict.html', predict=predict)
