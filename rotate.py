import os
import glob
from shutil import move
from xml.dom import minidom
import pandas as pd
import xml.etree.ElementTree as ET
from os import path

all_files = os.listdir(os.path.abspath("/Users/olivereielson/Desktop/new_data"))





for g in glob.glob('/Users/olivereielson/Desktop/new_data/*.JPG'):

    #file=g
    move(g,g.replace("new_data","random_image"))
    move(g.replace(".JPG",".xml"),g.replace("new_data","random_image").replace(".JPG",".xml"))
    #print(g.replace("new_data","random_image"))
    #print(file.replace("new_data","random_image").replace(".JPG",".xml"))




