import cv2
import os
import shutil

from pascal_voc_writer import Writer
from PIL import Image

f = open("/Users/olivereielson/Desktop/ball test/test_ball.txt", "r")

file = f.read()

files=file.split("\n")

show_image=True

current_index=0








while show_image:

    line=files[current_index]
    vals = line.split(",")

    img = cv2.imread(vals[4])

    xmin=int(vals[0])
    ymin=int(vals[1])
    xmax=int(vals[2])+int(vals[0])
    ymax=int(vals[1])-int(vals[3])


    cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (0, 0, 255), 2)


    if os.path.exists(vals[4].replace("ball test","check_over").replace(".jpg",".xml")):
        cv2.rectangle(img,(10,10),(200,60),(0,255,0),10)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    cv2.putText(img,str(current_index)+"---"+str(files.__len__()) , (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 5, 255)

    cv2.imshow("Image", img)
    t=cv2.waitKey(0)

    if t == 115:
        current_index = current_index + 1

    if t==32:

        try:
            os.remove(vals[4].replace("ball test","check_over"))
            os.remove(vals[4].replace("ball test","check_over").replace(".jpg",".xml"))
        except:
            print("error")

    if t==97:

        if current_index>0:
            current_index=current_index-1


    elif t==100:

        image= Image.open(vals[4])
        width, height = image.size

        writer = Writer(vals[4], width, height)
        writer.addObject("Squash", xmin, ymin, xmax, ymax)
        writer.save(vals[4].replace(".jpg",".xml").replace("ball test","check_over"))
        shutil.copyfile(vals[4], vals[4].replace("ball test","check_over"))


        if current_index<len(files)-1:
            current_index=current_index+1


