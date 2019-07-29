'''
@Description: View file for main blueprint
@Author: Tianyi Lu
@Date: 2019-07-05 17:27:28
@LastEditors: Tianyi Lu
@LastEditTime: 2019-07-29 17:46:06
'''

from flask import render_template, session, redirect, url_for, current_app, flash, request, Markup, abort
from .. import db
from . import main
from resnet152_transfer import res_transfer

@main.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')
