import cv2
import random
import glob
from PIL import Image

vids = glob.glob("/Users/olivereielson/Desktop/squashballs/*.MP4")

count2 = 0

for videos in vids:
    count2 += 1
    vidcap = cv2.VideoCapture(videos)
    success, image = vidcap.read()
    count = 0
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    while success:
        success, image = vidcap.read()

        cv2.imwrite(image,)

        count += 1
