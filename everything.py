import os
from distutils.dir_util import copy_tree
import shutil
import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
from random import shuffle
from math import floor

from smart_record import save_cvs, get_training_and_testing_sets

coner=False



if os.path.exists("OUTPUTS/test_labels.csv"):
    os.remove("OUTPUTS/test_labels.csv")
    print("OUTPUTS/test_labels.csv")


if os.path.exists("OUTPUTS/train_labels.csv"):
    os.remove("OUTPUTS/train_labels.csv")
    print("OUTPUTS/train_labels.csv")


if os.path.exists("OUTPUTS/train.record"):
    os.remove("OUTPUTS/train.record")
    print("OUTPUTS/train.record")




if os.path.exists("OUTPUTS/test.record"):
    os.remove("OUTPUTS/test.record")
    print("removed OUTPUTS/test.record")


if os.path.exists("OUTPUTS/label_map.pbtxt"):
    os.remove("OUTPUTS/label_map.pbtxt")
    print("removed OUTPUTS/label_map.pbtxt")


def label_map_v1(objname, number):
    with open('OUTPUTS/label_map.pbtxt', 'a') as the_file:
        the_file.write('item\n')
        the_file.write('{\n')
        the_file.write('id :{}'.format(int(number)))
        the_file.write('\n')
        the_file.write("name :'{0}'".format(objname))
        the_file.write('\n')
        the_file.write('}\n')


label_map_v1("Squash", 1)
label_map_v1("R_top_right", 2)
label_map_v1("R_top_left", 3)
label_map_v1("R_bottom_right", 4)
label_map_v1("R_bottom_left", 5)
label_map_v1("R_tin_bottom", 6)
label_map_v1("R_service_line", 7)
label_map_v1("R_conner_top", 8)
label_map_v1("L_top_right", 9)
label_map_v1("L_top_left", 10)
label_map_v1("L_bottom_right", 11)
label_map_v1("L_bottom_left", 12)
label_map_v1("L_tin_bottom", 13)
label_map_v1("L_service_line", 14)
label_map_v1("L_conner_top", 15)

# make CVS
if coner:

    all_files = glob.glob('/Users/olivereielson/Desktop/coners/*.xml')
else:
    all_files = glob.glob('/Volumes/Extra_Storage/new_data/*.xml')

files=[]

print(len(all_files))

for f in all_files:
    r=f.split("/")[-1]

    if os.path.exists(f.replace("xml","jpg")):
        files.append("/Users/olivereielson/Desktop/xml/"+r)
    else:
        print("bad file: "+f.replace("xml","jpg"))


    if not os.path.exists("/Users/olivereielson/Desktop/xml/"+r):
        shutil.copy(f, "/Users/olivereielson/Desktop/xml/"+r)

shuffle(files)
shuffle(files)


train,test =get_training_and_testing_sets(files,0.2)


save_cvs(test,"OUTPUTS/test_labels.csv")
print("saved test cvs")
save_cvs(train,"OUTPUTS/train_labels.csv")
print("saved train cvs")

# Make tf record

if coner:
    print("starting train.record")

    os.system('python generate.py  --csv_input=OUTPUTS/train_labels.csv  --output_path=OUTPUTS/train.record  --label_map=OUTPUTS/label_map.pbtxt --img_path=/Users/olivereielson/Desktop/coners')

    print("starting test.record ")

    os.system('python generate.py  --csv_input=OUTPUTS/test_labels.csv  --output_path=OUTPUTS/test.record  --label_map=OUTPUTS/label_map.pbtxt --img_path=//Users/olivereielson/Desktop/coners')
else:
    print("starting train.record ")

    os.system('python generate.py  --csv_input=OUTPUTS/train_labels.csv  --output_path=OUTPUTS/train.record  --label_map=OUTPUTS/label_map.pbtxt --img_path=/Volumes/Extra_Storage/new_data')
    print("starting test.record ")

    os.system('python generate.py  --csv_input=OUTPUTS/test_labels.csv  --output_path=OUTPUTS/test.record  --label_map=OUTPUTS/label_map.pbtxt --img_path=/Volumes/Extra_Storage/new_data')
