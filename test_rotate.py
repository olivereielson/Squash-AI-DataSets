import cv2
import os
import shutil
import numpy as np
import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
from random import shuffle
from math import floor

from pascal_voc_writer import Writer
from PIL import Image
import glob

shutil.rmtree('/Users/olivereielson/Desktop/ball test')
os.makedirs('/Users/olivereielson/Desktop/ball test')


show_image=True

current_index=0


class Rotate:
    '''
    Rotates images counter-clockwise by 90, 180, or 270 degrees.
    '''

    def __init__(self,
                 angle,
                 labels_format={'class_id': 0, 'xmin': 1, 'ymin': 2, 'xmax': 3, 'ymax': 4}):
        '''
        Arguments:
            angle (int): The angle in degrees by which to rotate the images counter-clockwise.
                Only 90, 180, and 270 are valid values.
            labels_format (dict, optional): A dictionary that defines which index in the last axis of the labels
                of an image contains which bounding box coordinate. The dictionary maps at least the keywords
                'xmin', 'ymin', 'xmax', and 'ymax' to their respective indices within last axis of the labels array.
        '''

        if not angle in {90, 180, 270}:
            raise ValueError("`angle` must be in the set {90, 180, 270}.")
        self.angle = angle
        self.labels_format = labels_format

    def __call__(self, image, labels=None):

        img_height, img_width = image.shape[:2]

        # Compute the rotation matrix.
        M = cv2.getRotationMatrix2D(center=(img_width / 2, img_height / 2),
                                    angle=self.angle,
                                    scale=1)

        # Get the sine and cosine from the rotation matrix.
        cos_angle = np.abs(M[0, 0])
        sin_angle = np.abs(M[0, 1])

        # Compute the new bounding dimensions of the image.
        img_width_new = int(img_height * sin_angle + img_width * cos_angle)
        img_height_new = int(img_height * cos_angle + img_width * sin_angle)

        # Adjust the rotation matrix to take into account the translation.
        M[1, 2] += (img_height_new - img_height) / 2
        M[0, 2] += (img_width_new - img_width) / 2

        # Rotate the image.
        image = cv2.warpAffine(image,
                               M=M,
                               dsize=(img_width_new, img_height_new))

        if labels is None:
            return image
        else:
            xmin = self.labels_format['xmin']
            ymin = self.labels_format['ymin']
            xmax = self.labels_format['xmax']
            ymax = self.labels_format['ymax']

            labels = np.copy(labels)
            # Rotate the bounding boxes accordingly.
            # Transform two opposite corner points of the rectangular boxes using the rotation matrix `M`.
            toplefts = np.array([labels[:,xmin], labels[:,ymin], np.ones(labels.shape[0])])
            bottomrights = np.array([labels[:,xmax], labels[:,ymax], np.ones(labels.shape[0])])
            new_toplefts = (np.dot(M, toplefts)).T
            new_bottomrights = (np.dot(M, bottomrights)).T
            labels[:,[xmin,ymin]] = np.round(new_toplefts, decimals=0).astype(np.int)
            labels[:,[xmax,ymax]] = np.round(new_bottomrights, decimals=0).astype(np.int)

            if self.angle == 90:
                # ymin and ymax were switched by the rotation.
                labels[:,[ymax,ymin]] = labels[:,[ymin,ymax]]
            elif self.angle == 180:
                # ymin and ymax were switched by the rotation,
                # and also xmin and xmax were switched.
                labels[:,[ymax,ymin]] = labels[:,[ymin,ymax]]
                labels[:,[xmax,xmin]] = labels[:,[xmin,xmax]]
            elif self.angle == 270:
                # xmin and xmax were switched by the rotation.
                labels[:,[xmax,xmin]] = labels[:,[xmin,xmax]]

            return image, labels


length= len(glob.glob("/Users/olivereielson/Desktop/check_over/*.xml"))
current=0
for g in glob.glob("/Users/olivereielson/Desktop/check_over/*.xml"):

    if os.path.exists(g.replace(".xml",".jpg")):
        current=current+1
        print(str(current)+"---"+str(length))
        img=cv2.imread(g.replace(".xml",".jpg"))
        #print(img.shape)

        tree = ET.parse(g)
        root = tree.getroot()
        for member in root.findall("object"):

            value = (
                root.find("filename").text.replace(".HEIC", ".jpg").replace(".jpeg", ".jpg").replace(".png", ".jpg"),
                floor(float(root.find("size")[0].text)),
                floor(float(root.find("size")[1].text)),
                member[0].text,
                floor(float(member[4][0].text)),
                floor(float(member[4][1].text)),
                floor(float(member[4][2].text)),
                floor(float(member[4][3].text)),
            )
            if member[0].text == "Squash":
                #print(value)
                rotate = Rotate(angle=270, )
                image, label = rotate(img, labels=[[0, value[4], value[5], value[6], value[7]]])
                #print(label)
                #cv2.rectangle(image,(label[0][1],label[0][2]),(label[0][3],label[0][4]),color=(255,0,0),thickness=5)
                writer = Writer(g.replace(".xml", ".jpg"), image.shape[1], image.shape[0])
                writer.addObject("Squash", label[0][1], label[0][2], label[0][3], label[0][4])

                writer.save("/Users/olivereielson/Desktop/ball test/"+g.split("/")[-1])
                cv2.imwrite("/Users/olivereielson/Desktop/ball test/"+g.split("/")[-1].replace(".xml", ".jpg"), image)



        #cv2.imshow("Image", image)


shutil.rmtree('/Users/olivereielson/Desktop/check_over')
os.makedirs('/Users/olivereielson/Desktop/check_over')




