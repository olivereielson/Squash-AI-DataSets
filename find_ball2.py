import os
import shutil
import random

import numpy as np
import cv2
from datetime import datetime
import glob

shutil.rmtree('/Users/olivereielson/Desktop/ball test')
os.makedirs('/Users/olivereielson/Desktop/ball test')


Back_Hand=False

for file in glob.glob("/Volumes/Extra_Storage/SOLO VIDEO/find_ball/ForeHand/*.MP4"):

    cap = cv2.VideoCapture(file)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count = 0
    save_count=0
    back_sub = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=100, detectShadows=False)

    kernel = np.ones((20, 20), np.uint8)

    params = cv2.SimpleBlobDetector_Params()


    params.minDistBetweenBlobs = 300

    # Set Area filtering parameters
    params.filterByArea = True
    params.minArea = 10

    # Set Circularity filtering parameters


    detector = cv2.SimpleBlobDetector_create(params)



    frame_old = cv2.imread("../S_Project/test.jpg")


    try:

        while (cap.isOpened()):
            frame_count = frame_count + 1
            ret, frame = cap.read()

            if frame_count==1 or frame_count%60==0:
                frame_old=frame.copy()
                print("new frame")



            difference = cv2.subtract(frame_old, frame)
            Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            areas = [cv2.contourArea(c) for c in contours]

            height, width = frame.shape[:2]



            cv2.imshow('frame2',mask)
            #cv2.imshow('frame3',fg_mask_bb)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except:
        print("done")

    cap.release()
    cv2.destroyAllWindows()




