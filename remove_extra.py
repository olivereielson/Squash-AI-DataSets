import os
import glob
from shutil import copyfile
from xml.dom import minidom
import pandas as pd
import xml.etree.ElementTree as ET
from os import path

all_files = os.listdir(os.path.abspath("/Users/olivereielson/Desktop/new_data"))





for g in glob.glob('/Users/olivereielson/Desktop/new_data/*.jpg'):




    if path.exists(g.replace(".jpg",".xml"))==False:
        os.remove(g)



for g in glob.glob('/Users/olivereielson/Desktop/new_data/*.JPG'):




    if path.exists(g.replace(".JPG",".xml"))==False:
        os.remove(g)


