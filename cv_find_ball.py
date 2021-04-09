import os
import shutil
import random

import numpy as np
import cv2
from datetime import datetime
import glob

shutil.rmtree('/Users/olivereielson/Desktop/ball test')
os.makedirs('/Users/olivereielson/Desktop/ball test')


Back_Hand=True

#for file in glob.glob("/Volumes/Extra_Storage/SOLO VIDEO/find_ball/ForeHand/*.MP4"):
for file in glob.glob("/Users/olivereielson/Desktop/i/*.MP4"):

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

    def pointInRect(point,rect):
        x1, y1, w, h = rect
        x2, y2 = x1+w, y1+h
        x, y = point
        if (x1 < x and x < x2):
            if (y1 < y and y < y2):
                return True
        return False

    detector = cv2.SimpleBlobDetector_create(params)



    def rotate(point, origin, degrees):
        radians = np.deg2rad(degrees)
        x,y = point
        offset_x, offset_y = origin
        adjusted_x = (x - offset_x)
        adjusted_y = (y - offset_y)
        cos_rad = np.cos(radians)
        sin_rad = np.sin(radians)
        qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
        return int(qx), int(qy)



    try:

        while (cap.isOpened()):
            frame_count = frame_count + 1



            ret, frame = cap.read()


            height, width = frame.shape[:2]

            #print(height)

            frame=cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)



            fg_mask = back_sub.apply(frame)

            if Back_Hand:
                fg_mask=cv2.flip(fg_mask,0)


            # Close dark gaps in foreground object using closing
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

            # Remove salt and pepper noise with a median filter
            fg_mask = cv2.medianBlur(fg_mask, 5)

            # Threshold the image to make it either black or white
            _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY_INV)

            # Find the index of the largest contour and draw bounding box
            fg_mask_bb = fg_mask
            contours, hierarchy = cv2.findContours(fg_mask_bb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            areas = [cv2.contourArea(c) for c in contours]


            areas.sort()




            if len(areas) < 1:

                # Display the resulting frame
                #cv2.imshow('frame', frame)

                # If "q" is pressed on the keyboard,
                # exit this loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Go to the top of the while loop
                continue

            else:
                # Find the largest moving object in the image
                max_index = np.argmax(areas)




            #keypoints = detector.detect(fg_mask_bb)

            #keypoints2 = []
            cnt = contours[max_index]

            x, y, w, h = cv2.boundingRect(cnt)




            if w < 8:
                x=x-4
                w=w+4

            if h < 8:
                y=y-4
                h=h+4

            #blank = np.zeros((1, 1))
            #blobs = cv2.drawKeypoints(fg_mask_bb, keypoints2, blank, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            height, width, channels = frame.shape# float `height`

            #print(y)

            #x,y= rotate((x,y),(width/2,height/2),270)

            #print(y)




            #frame=cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)


            cut0ff=0
            cutOff2=3000

            slope=(850-0)/(cut0ff-cutOff2)

            y_prime=slope*(x-cut0ff)+850




            if h<200 and w<200 and x>cut0ff:


                save_count=save_count+1

                if save_count %13 ==0:
                    file_name = str(frame_count) + "--" + str(datetime.now()).replace(".", "-").replace(" ", "-").replace("/", "-").replace("/", "-")
                    cv2.imwrite("/Users/olivereielson/Desktop/ball test/" + file_name + ".jpg", frame)
                    f = open("/Users/olivereielson/Desktop/ball test/test_ball.txt", "a")

                    if Back_Hand:

                        f.write(str(x) + "," + str(height-y) + "," + str(w) + ","+ str(h) + ",/Users/olivereielson/Desktop/ball test/" + file_name + ".jpg\n")
                    else:
                        f.write(str(x) + "," + str(y) + "," + str(w) + ","+ str(h) + ",/Users/olivereielson/Desktop/ball test/" + file_name + ".jpg\n")

                    f.close()


                if Back_Hand:
                    cv2.rectangle(frame, (x, height-y), (x + w, (height-y) - h), (0, 255, 0), 5)
                else:
                    cv2.rectangle(frame, (x, y), (x + w,y+ h), (0, 255, 0), 5)



            #cv2.line(frame,(cut0ff,850),(cutOff2,0),thickness=50,color=(0,255,0))
            cv2.line(frame,(cut0ff,0),(cut0ff,2500),thickness=50,color=(0,255,0))
            #cv2.line(frame,(cutOff2,0),(cutOff2,2500),thickness=50,color=(0,255,0))


            #cv2.rectangle(blobs, (x, y), (x + w, y + h), (0, 255, 0), 5)
            frame = cv2.resize(frame,(300,300))
            #cv2.imshow('frame',fg_mask_bb)
            cv2.putText(frame,str(frame_count)+"---"+str(length)+"----"+str((frame_count/length)*100)+"%" , (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, 255)



            cv2.imshow('frame2',frame)
            #cv2.imshow('frame3',fg_mask_bb)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except:
        print("done")

    cap.release()
    cv2.destroyAllWindows()




