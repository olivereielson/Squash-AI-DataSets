import os
import shutil
import random
from pascal_voc_writer import Writer
import numpy as np
import cv2
from datetime import datetime

# shutil.rmtree('/Users/olivereielson/Desktop/coners')
# os.makedirs('/Users/olivereielson/Desktop/coners')


R_top_right = (2385, 750)
R_top_left = (2385, 1540)
R_bottom_right = (2550, 600)
R_bottom_left = (2550, 1670)

points = [[2385, 750], [2385, 1540], [2550, 600], [2550, 1670], [2200, 800], [1800, 800],  [1800, 800]   ]

#names = ["R_top_right", "R_top_left", "R_bottom_right", "R_bottom_left", "R_tin_bottom", "R_service_line", "R_conner_top",]
names = ["L_top_right", "L_top_left", "L_bottom_right", "L_bottom_left", "L_tin_bottom", "L_service_line","L_conner_top"]

box_size = 9

vid_file = "/Users/olivereielson/Desktop/52BB762C-38C0-431E-AF2D-225AC505D2D0.MP4"
cap = cv2.VideoCapture(vid_file)

length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

frame_count = 0
save_count = 0
p_index = 0
testing = True
finding = True
back_sub = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=70, detectShadows=False)

kernel = np.ones((20, 20), np.uint8)


def mouse_click(event, x, y, flags, param):
    global p_index
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        frame3 = cv2.imread("../S_Project/test.jpg")
        frame3 = cv2.resize(frame3, (900, 900))

        print(p_index)
        points[p_index] = [x, y]
        cv2.circle(frame3, (points[p_index][0], points[p_index][1]), box_size, (255, 0, 0), thickness=2)
        cv2.imshow('frames2', frame3, )


while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imwrite("../S_Project/test.jpg", frame)
    while finding:
        frame2 = cv2.imread("../S_Project/test.jpg")

        frame = cv2.resize(frame, (900, 900))
        frame2 = cv2.resize(frame2, (900, 900))

        cv2.imshow('frames2', frame, )

        cv2.setMouseCallback('frames2', mouse_click)

        cv2.circle(frame2, (points[p_index][0], points[p_index][1]), box_size, (255, 0, 0), thickness=5)

        t = cv2.waitKey(0)

        if t == 3:
            points[p_index][0] = points[p_index][0] + 5
        if t == 2:
            points[p_index][0] = points[p_index][0] - 5
        if t == 0:
            points[p_index][1] = points[p_index][1] - 5
        if t == 1:
            points[p_index][1] = points[p_index][1] + 5
        if t == 32:
            if p_index == len(points)-1:
                finding = False

            p_index = p_index + 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    break

cap.release()
cv2.destroyAllWindows()

f = open("OUTPUTS/corner.txt", "a")

f.write("\n"+str(points)+"-"+str(names)+"-"+vid_file)

f.close()

frame_old = cv2.imread("../S_Project/test.jpg")
frame_old = cv2.resize(frame_old, (900, 900))
diff_frame = frame_old.copy()
un_frame = frame_old.copy()

cap = cv2.VideoCapture(vid_file)

#*
fgbg = cv2.createBackgroundSubtractorMOG2()

while (cap.isOpened()):

    frame_count = frame_count + 1
    ret, frame = cap.read()
    frame = cv2.resize(frame, (900, 900))

    show = frame.copy()


    # color the mask red

    if frame_count % 200 == 0 and testing:

        un_frame = frame.copy()

        for i in range(len(points)):
            cv2.circle(un_frame, (points[i][0], points[i][1]), box_size, (0, 200, 0), thickness=1)

        difference = cv2.subtract(frame_old, frame)
        Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        difference[mask != 255] = [0, 0, 255]
        diff_frame = difference.copy()


        channels = cv2.mean(diff_frame)
        observation = np.array([(channels[2], channels[1], channels[0])])

        if observation[0].mean() < 200:

            height, width = frame.shape[:2]
            file_name = str(frame_count) + "--" + str(datetime.now()).replace(".", "-").replace(" ", "-").replace("/", "-").replace("/", "-")
            cv2.imwrite("/Users/olivereielson/Desktop/coners/" + file_name + ".jpg", frame)

            writer = Writer("/Users/olivereielson/Desktop/coners/" + file_name + ".jpg", width, height)

            for i in range(len(points)):

                crop_img = diff_frame[(points[i][1] - box_size):(points[i][1] + box_size), (points[i][0] - box_size):(points[i][0] + box_size)]

                channels = cv2.mean(crop_img)
                observation = np.array([(channels[2], channels[1], channels[0])])

                if channels[2] < 20:
                    # cv2.circle(diff_frame, (points[i][0], points[i][1]), box_size, (255, 0, 0), thickness=5)

                    cv2.rectangle(diff_frame, (points[i][0] - box_size, points[i][1] - box_size), (points[i][0] + box_size, points[i][1] + box_size), (255, 0, 0), thickness=1)

                    cv2.circle(un_frame, (points[i][0], points[i][1]), box_size, (255, 0, 0), thickness=2)
                    writer.addObject(names[i], points[i][0] - box_size, points[i][1] - box_size, points[i][0] + box_size, points[i][1] + box_size)

                else:
                    print(channels[2])

            writer.save("/Users/olivereielson/Desktop/coners/" + file_name + ".xml")

            cv2.putText(diff_frame, str(frame_count) + "---" + str(length) + "----" + str((frame_count / length) * 100) + "%", (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, 255)

    frame = cv2.resize(show, (500, 500))

    # cv2.imshow('fd', fg_mask)

    cv2.imshow('frame2', un_frame)
    cv2.imshow('diff.png', diff_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

""""

while (cap.isOpened()):

    frame_count = frame_count + 1
    ret, frame = cap.read()
    frame = cv2.resize(frame, (900, 900))

    fg_mask = back_sub.apply(frame)

    # Close dark gaps in foreground object using closing
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

    # Remove salt and pepper noise with a median filter
    fg_mask = cv2.medianBlur(fg_mask, 5)

    # Threshold the image to make it either black or white
    _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY_INV)

    show = frame.copy()

    for i in range(len(points)):
        cv2.circle(show, (points[i][0], points[i][1]), box_size, (0, 200, 0), thickness=5)

    if frame_count % 30 == 0 and testing:
        height, width = frame.shape[:2]
        file_name = str(frame_count) + "--" + str(datetime.now()).replace(".", "-").replace(" ", "-").replace("/", "-").replace("/", "-")
        cv2.imwrite("/Users/olivereielson/Desktop/coners/" + file_name + ".jpg", frame)

        writer = Writer("/Users/olivereielson/Desktop/coners/" + file_name + ".jpg", width, height)

        for i in range(len(points)-1):


            crop_img = fg_mask[(points[i][1] - box_size):(points[i][1] + box_size), (points[i][0] - box_size):(points[i][0] + box_size)]

            h, w = crop_img.shape[:2]
            cv2.imshow('fsdd', crop_img)

            val=1
            ave_len=0

            for y in range((box_size*2)-1):
                for x in range((box_size*2)-1):
                    pixel = crop_img[x][y]
                    val=pixel+val
                    ave_len=ave_len+1

            print(val)
            print(ave_len)
            print(h)
            print(w)

            if val/ave_len>200:
                cv2.circle(show, (points[i][0], points[i][1]), box_size, (255, 0, 0), thickness=5)
                writer.addObject(names[i], points[i][0] - box_size, points[i][1] - box_size, points[i][0] + box_size, points[i][1] + box_size)

        writer.save("/Users/olivereielson/Desktop/coners/" + file_name + ".xml")

    cv2.putText(show, str(frame_count) + "---" + str(length) + "----" + str((frame_count / length) * 100) + "%", (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, 255)

    frame = cv2.resize(show, (500, 500))
    # fg_mask = cv2.resize(fg_mask,(500,500))

    cv2.imshow('fd', fg_mask)

    cv2.imshow('frame2', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

"""