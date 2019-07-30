import cv2
import os
from PIL import Image

def get_cover(path):
    abs_path = os.path.abspath('.')
    abs_path = os.path.join(abs_path, 'app/static/video_cover')
    vc = cv2.VideoCapture(path)
    rval = vc.isOpened()
    rval, frame = vc.read()
    bgr_img = Image.fromarray(frame)
    b, g, r = bgr_img.split()
    rgb_img = Image.merge('RGB', (r,g,b))
    name = path.split('/')[-1].split('.')[0]+'.jpg'
    abs_path = os.path.join(abs_path,name)
    rgb_img.save(abs_path)

    return name

if __name__ == '__main__':
    print(get_cover('balloon_scissor.mp4'))
