'''
@Description: View file for main blueprint
@Author: Tianyi Lu
@Date: 2019-07-05 17:27:28
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-29 19:02:53
'''
import os
from flask import render_template, session, redirect, url_for, current_app, flash, request, Markup, abort
from .. import db
from . import main
from resnet152_transfer import res_transfer

path1 = os.path.abspath('./app')

@main.route('/', methods=['GET', 'POST'])
def index():
    data_dir = os.path.join(path1, 'static/user_img/01')
    print(data_dir)
    predict = res_transfer.predict(data_dir, '2019-07-29-01')
    print(predict)
    return render_template('index.html')
