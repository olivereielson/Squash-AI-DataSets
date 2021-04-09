import os
import shutil
import random
from pascal_voc_writer import Writer
import numpy as np
import cv2
from datetime import datetime

# shutil.rmtree('/Users/olivereielson/Desktop/coners')
# os.makedirs('/Users/olivereielson/Desktop/coners')





f = open("OUTPUTS/corner.txt", "r")
lines=f.read().split("\n")

for line in lines:
    points = []

    p=line.split("--")[0].replace("[","").replace("]","").replace(" ","").split(",")

    #print(p)

    for i in range(int(len(p)/2)):
        points.append([int(p[i*2]),int(p[(i*2)+1])])



    names=line.split("--")[1].replace("[","").replace("]","").replace(" ","").replace("'","").split(",")

    print(names)


    print(points)

    box_size = 5

    vid_file = line.split("--")[-1]

    cap = cv2.VideoCapture(vid_file)




    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count = 0
    save_count = 0
    p_index = 0
    testing = True
    finding = True
    back_sub = cv2.createBackgroundSubtractorMOG2(history=1000, varThreshold=70, detectShadows=False)

    kernel = np.ones((20, 20), np.uint8)


    while (cap.isOpened()):
        ret, frame = cap.read()
        cv2.imwrite("../S_Project/test.jpg", frame)
        break

    print("here")




    cap.release()
    cv2.destroyAllWindows()

    cap = cv2.VideoCapture(vid_file)


    try:
        while (cap.isOpened()):

            frame_count = frame_count + 1
            ret, frame = cap.read()
            frame = cv2.resize(frame, (900, 900))



            show = frame.copy()





            # color the mask red






            if frame_count % 30 == 0 and testing:

                un_frame=frame.copy()

                for i in range(len(points)):
                    cv2.circle(un_frame, (points[i][0], points[i][1]), box_size, (0, 200, 0), thickness=1)

                difference = cv2.subtract(frame_old, frame)
                Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
                difference[mask != 255] = [0, 0, 255]
                diff_frame=difference.copy()

                channels = cv2.mean(diff_frame)
                observation = np.array([(channels[2], channels[1], channels[0])])

                #frame_old=frame
                if observation[0].mean() < 200:

                    height, width = frame.shape[:2]
                    file_name = str(frame_count) + "--" + str(datetime.now()).replace(".", "-").replace(" ", "-").replace("/", "-").replace("/", "-")
                    cv2.imwrite("/Users/olivereielson/Desktop/coners/" + file_name + ".jpg", frame)

                    writer = Writer("/Users/olivereielson/Desktop/coners/" + file_name + ".jpg", width, height)

                    for i in range(len(points)):


                        crop_img = diff_frame[(points[i][1] - box_size):(points[i][1] + box_size), (points[i][0] - box_size):(points[i][0] + box_size)]

                        channels = cv2.mean(crop_img)
                        observation = np.array([(channels[2], channels[1], channels[0])])

                        if channels[2]<20:
                            #cv2.circle(diff_frame, (points[i][0], points[i][1]), box_size, (255, 0, 0), thickness=5)

                            cv2.rectangle(diff_frame,(points[i][0] - box_size, points[i][1] - box_size),(points[i][0] + box_size, points[i][1] + box_size), (255, 0, 0), thickness=1)


                            cv2.circle(un_frame, (points[i][0], points[i][1]), box_size, (255, 0, 0), thickness=2)
                            writer.addObject(names[i], points[i][0] - box_size, points[i][1] - box_size, points[i][0] + box_size, points[i][1] + box_size)

                        else:
                            print(channels[2])

                    writer.save("/Users/olivereielson/Desktop/coners/" + file_name + ".xml")

                    cv2.putText(diff_frame, str(frame_count) + "---" + str(length) + "----" + str((frame_count / length) * 100) + "%", (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, 255)


            frame = cv2.resize(show, (500, 500))

            #cv2.imshow('fd', fg_mask)

            cv2.imshow('frame2', un_frame)
            cv2.imshow('diff.png', diff_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    except:
        print("done")