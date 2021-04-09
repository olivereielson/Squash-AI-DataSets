import cv2
import os
import shutil
from pascal_voc_writer import Writer
from PIL import Image
import tensorflow as tf
import glob



file=glob.glob("/Users/olivereielson/Desktop/new_data/*.xml")


Squash = tf.lite.Interpreter(model_path="converted_model.tflite")

input_details_squash = Squash.get_input_details()
output_details_squash = Squash.get_output_details()

# people.allocate_tensors()
Squash.allocate_tensors()




show_image = True

current_index = 0

while show_image:

    frame = cv2.imread(str(file[current_index]).replace(".xml",".jpg"))

    Squash.set_tensor(input_details_squash[0]['index'], [frame])

    Squash.invoke()
    rects = Squash.get_tensor(output_details_squash[0]['index'])
    clas = Squash.get_tensor(output_details_squash[1]['index'])
    scores = Squash.get_tensor(output_details_squash[2]['index'])

    xmin = int(rects[0][0][0])
    ymin = int(rects[0][0][1])
    xmax = int(rects[0][0][2])
    ymax = int(rects[0][0][3])

    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

    if os.path.exists(vals[4].replace("ball test", "check_over").replace(".jpg", ".xml")):
        cv2.rectangle(img, (10, 10), (200, 60), (0, 255, 0), 10)

    cv2.imshow("Image", img)
    t = cv2.waitKey(0)

    if t == 115:
        current_index = current_index + 1

    if t == 32:

        try:
            os.remove(vals[4].replace("ball test", "check_over"))
            os.remove(vals[4].replace("ball test", "check_over").replace(".jpg", ".xml"))
        except:
            print("error")

    if t == 97:

        if current_index > 0:
            current_index = current_index - 1


    elif t == 100:

        image = Image.open(vals[4])
        width, height = image.size

        writer = Writer(vals[4], width, height)
        writer.addObject("Squash", xmin, ymin, xmax, ymax)
        writer.save(vals[4].replace(".jpg", ".xml").replace("ball test", "check_over"))
        shutil.copyfile(vals[4], vals[4].replace("ball test", "check_over"))

        if current_index < len(files) - 1:
            current_index = current_index + 1


