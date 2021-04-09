import glob
import os
import shutil
import random

import tensorflow as tf
import xml.etree.ElementTree as ET
import cv2
from PIL import Image
from pascal_voc_writer import Writer
import numpy as np

size = 300
working=True
file_index=0

Squash = tf.lite.Interpreter(model_path="ssd_mobilenet.tflite")

input_details_squash = Squash.get_input_details()
output_details_squash = Squash.get_output_details()

Squash.allocate_tensors()

def draw_box(frame, box):
    y_min = int(max(1, (box[0] * size)))
    x_min = int(max(1, (box[1] * size)))
    y_max = int(min(size, (box[2] * size)))
    x_max = int(min(size, (box[3] * size)))

    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

xml_files = glob.glob("/Users/olivereielson/Desktop/new_data/*.xml")
random.shuffle(xml_files)

while working:

    xml_file=xml_files[file_index]
    tree = ET.parse(xml_file)
    root = tree.getroot()

    file_root_name=xml_file.split("/")[-1]

    if os.path.exists(xml_file) and os.path.exists(xml_file.replace("xml","jpg")):

        old_val = []

        for member in root.findall("object"):


            value = (
                root.find("filename").text.replace(".HEIC", ".jpg").replace(".jpeg", ".jpg").replace(".png", ".jpg"),
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text),
            )
            old_val.append(value)


        #print(old_val)
        img_file=xml_file.replace(".xml",".jpg")
        image=cv2.imread(img_file)

        image=cv2.resize(image,(300,300))

        frame=image.copy()

        #image = image.astype(np.float32)
        #image /= 255.
        Squash.set_tensor(input_details_squash[0]['index'], [image])
        Squash.invoke()
        rects = Squash.get_tensor(output_details_squash[0]['index'])
        scores = Squash.get_tensor(output_details_squash[2]['index'])

        print(scores[0][0])

        for idx,s in enumerate(scores[0]):

            if s>0.6:

                draw_box(image, rects[0][idx])


                t=9012320



                if t==6:
                    image2 = Image.open(img_file)
                    width, height = image2.size
                    print(file_root_name)
                    writer = Writer(file_root_name.replace("xml","jpg"), width, height)


                    for val in old_val:
                        line=str(val).replace("'","").replace(" ","").replace(")","").split(",")
                        writer.addObject(line[3], line[4], line[5], line[6], line[7])



                    writer.addObject("Racquet", int(rects[0][0][1]*width), int(rects[0][0][0]*height), int(rects[0][0][3]*width), int(rects[0][0][2]*height))
                    writer.save("/Users/olivereielson/Desktop/saved_rac/"+file_root_name)
                    file_index=file_index+1


                if t == 115:
                    shutil.copyfile(img_file,"/Users/olivereielson/Desktop/man_edit/"+file_root_name.replace("xml","jpg") )
                    file_index = file_index + 1

                if t==32:

                    try:
                        os.remove("/Users/olivereielson/Desktop/saved_rac/"+file_root_name)
                        os.remove("/Users/olivereielson/Desktop/saved_rac/"+file_root_name.replace("xml","jpg"))
                    except:
                        print("error")

                if t==97:

                    if file_index>0:
                        file_index=file_index-1


                elif t==100:

                    image2= Image.open(img_file)
                    width, height = image2.size

                    writer = Writer(img_file, width, height)
                    writer.addObject("Racquet", rects[0][0][1]*width, rects[0][0][0]*height, rects[0][0][3]*width, rects[0][0][2]*height)
                    writer.save("/Users/olivereielson/Desktop/saved_rac/"+file_root_name)

                    cv2.imwrite("/Users/olivereielson/Desktop/saved_rac/"+file_root_name.replace("xml","jpg"),frame)

                    #shutil.copyfile(img_file,"/Users/olivereielson/Desktop/saved_rac/"+file_root_name.replace("xml","jpg") )


                    file_index=file_index+1

            else:
                file_index=file_index+1

        cv2.imshow("image",image)

        cv2.waitKey(0)





