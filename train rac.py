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

coner=True

try:
    os.remove("OUTPUTS/test_labels.csv")
    os.remove("OUTPUTS/train_labels.csv")
except:
    print("error deleting OUTPUTS/train.record")
try:

    os.remove("OUTPUTS/train.record")
    print("removed OUTPUTS/train.record")


except:
    print("error deleting OUTPUTS/train.record")

try:
    os.remove("OUTPUTS/test.record")
    print("removed OUTPUTS/test.record")


except:
    print("error deleting OUTPUTS/test.record")

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


label_map_v1("Racquet", 1)


all_files = glob.glob('/Volumes/Extra_Storage/rac/*.xml')


files=[]

for f in all_files:
    if os.path.exists(f.replace("xml","jpg")):
        files.append(f)
    else:
        print("bad file: "+f.replace("xml","jpg"))


shuffle(files)
shuffle(files)


train,test =get_training_and_testing_sets(files,0.2)

save_cvs(test,"OUTPUTS/test_labels.csv")
print("saved test cvs")
save_cvs(train,"OUTPUTS/train_labels.csv")
print("saved train cvs")


print("starting train.record ")
os.system('python generate.py  --csv_input=OUTPUTS/train_labels.csv  --output_path=OUTPUTS/train.record  --label_map=OUTPUTS/label_map.pbtxt --img_path=/Volumes/Extra_Storage/rac')



print("starting test.record ")
os.system('python generate.py  --csv_input=OUTPUTS/test_labels.csv  --output_path=OUTPUTS/test.record  --label_map=OUTPUTS/label_map.pbtxt --img_path=/Volumes/Extra_Storage/rac')
