import os
from PIL import Image
import secrets
from flask import current_app
from datetime import datetime

# type与root path对应的字典，方便今后维护

def saver(dirname, form_picture):

    random_hex = secrets.token_hex(8)

    _, file_extension = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + file_extension

    i = Image.open(form_picture)


    moment_dir = os.path.join(current_app.root_path, current_app.config['IMG_PATH'], dirname)
    if not os.path.exists(moment_dir):
        os.mkdir(moment_dir)
        os.mkdir(os.path.join(moment_dir, 'img'))

    width, height = i.size

    # save picture of full size
    if width > 2000 or height > 2000:
        i.thumbnail([2000, 2000])
    print('test')
    full_picture_path = os.path.join(current_app.root_path, moment_dir, 'img',picture_file_name)
    i.save(full_picture_path)

    return picture_file_name

# def deleter(type, old_file_name, moment_dir=None): # moment_dir is the id of the group to which the moment belongs.
#     if moment_dir:
#         full_pic_path = os.path.join(current_app.root_path, root_path[type], str(moment_dir), old_file_name)
#         thumbnail_path = os.path.join(current_app.root_path, root_path[type], str(moment_dir), 'thumbnail_%s' % old_file_name)
#         os.remove(full_pic_path)
#         os.remove(thumbnail_path)
#     else:
#         old_file_path = os.path.join(current_app.root_path, root_path[type], old_file_name)
#         os.remove(old_file_path)
