'''
@Description: View file for main blueprint
@Author: Tianyi Lu
@Date: 2019-07-05 17:27:28
@LastEditors: Tianyi Lu
@LastEditTime: 2019-08-02 08:47:52
'''
import os
import json
from flask import render_template, session, redirect, url_for, current_app, flash, request, Markup, abort
from .. import db
from . import main
from flask_login import login_required, current_user
from resnet152_transfer import res_transfer
from ..image_saver import saver
from datetime import datetime
from ..models import PictureSet, Video, User, Comment
from random import randint

path1 = os.path.abspath('./app')

@main.route('/', methods=['GET', 'POST'])
def index():
    flash('Hello')
    video_dict = {}
    video_dict['easy'] = Video.query.filter_by(difficulties=0).all()[:9]
    video_dict['medium'] = Video.query.filter_by(difficulties=1).all()[:9]
    video_dict['hard'] = Video.query.filter_by(difficulties=2).all()[:9]


    slogan = current_app.config['SLOGAN'][randint(0, len(current_app.config['SLOGAN'])-1)]
    if request.method == 'POST':

        dt = datetime.utcnow()
        dt_string = dt.strftime("%Y-%m-%d-%H-%M-%S")
        pictures = request.files.getlist('pictures')
        if not pictures:
            keywords = request.form['search']
            print(keywords)
            return redirect(url_for('main.search', keywords=keywords))

        for picture in pictures:
            saver(dt_string, picture)

        return redirect(url_for('main.imageset', dirname=dt_string))
        
    return render_template('index.html', slogan=slogan, video_dict=video_dict)

@main.route('/video/<int:id>', methods=['GET', 'POST'])
@login_required
def video(id):
    v = Video.query.get_or_404(id)
    comments = Comment.query.filter_by(video_id=id).all()
    materials = eval(v.materials)
    if request.method == 'POST':
        content = request.form['content']
        c = Comment(author=current_user, video=v, content=content)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('main.video', id=id))
    return render_template('video.html', v=v, materials=materials, comments=comments)

@main.route('/video/upload', methods=['GET', 'POST'])
@login_required
def video_upload():
    return render_template('video_upload.html')

@main.route('/search')
@login_required
def search():

    res_videos = []
    keywords = request.args.get('keywords') or ''
    keywords_list = keywords.split(' ')
    keywords_list = list(set(keywords_list))
    for keyword in keywords_list:
        videos = [v for v in Video.query.msearch(keyword, fields=['materials', 'title']).all() if v not in res_videos]
        for video in videos:
            res_videos.append(video)

    return render_template('search.html', keywords_list=keywords_list, res_videos=res_videos)

@main.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user, id=id)

@main.route('/imageset/<dirname>', methods=['GET', 'POST'])
@login_required
def imageset(dirname):
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
    # print(predict)

    if request.method == 'POST':
        keys = [x for x in predict.keys()]
        for i in range(len(keys)):
            predict[keys[i]] = request.form[keys[i]]
        pictureset.prediction = json.dumps(predict)
        db.session.add(pictureset)
        db.session.commit()
        print(pictureset.prediction)
        keywords = ''.join([str(x)+' ' for x in predict.values()])
        keywords = keywords.strip()
        return redirect(url_for('main.search', keywords=keywords))
        
        
    return render_template('imageset.html', dirname=dirname, predict=predict)
