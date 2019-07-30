'''
@Description: View file for main blueprint
@Author: Tianyi Lu
@Date: 2019-07-05 17:27:28
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-30 08:33:24
'''
import os
import json
from flask import render_template, session, redirect, url_for, current_app, flash, request, Markup, abort
from .. import db
from . import main
from resnet152_transfer import res_transfer
from ..image_saver import saver
from datetime import datetime
from ..models import PictureSet, Video

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
    v = Video.query.get_or_404(id)
    materials = eval(v.materials)
    return render_template('video.html', v=v, materials=materials)

# @main.route('/search')
# def search():

#     res_videos = []
#     keywords = request.args.get('keywords') or ''
#     keywords_list = keywords.split(' ')
#     for keyword in keywords_list:
#         res_videos.append([v for v in Video.query.msearch(keyword, fields=['materials', 'title']).all() if v not in res_videos])

#     return render_template('search.html', keywords_list=keywords_list, res_videos=res_videos)


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

    # if request == 'POST':
    #     keywords = ''.join([str(x)+' ' for x in predict])
    #     print(keywords)
    #     return redirect(url_for('main.search', keywords=keywords))
        
        
    return render_template('imageset.html', dirname=dirname, predict=predict)
