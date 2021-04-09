import glob
import os
import shutil
from os import path

##
for g in glob.glob('/Users/olivereielson/Desktop/new_data/*.xml'):

    s = g.replace("/Users/olivereielson/Desktop/phone/", "")

    t = g.replace(".xml", ".JPG")

    r=g.replace("/Users/olivereielson/Desktop/new_data/","")

    if not path.exists(t):
        print(g)

        shutil.copyfile(g, "/Users/olivereielson/Desktop/not_good/" + r)
        os.remove(g)

##
