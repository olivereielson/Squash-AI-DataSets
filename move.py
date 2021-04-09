import os
import glob
from shutil import copyfile
from xml.dom import minidom
import pandas as pd
import xml.etree.ElementTree as ET

all_files = os.listdir(os.path.abspath("/Users/olivereielson/Desktop/man_edit"))




def move():

    for g in glob.glob('/Users/olivereielson/Desktop/man_edit/*.xml'):

        base_file=g.split("/")[-1]
        base_img=base_file.replace(".xml",".jpg")


        copyfile("/Users/olivereielson/Desktop/man_edit/"+base_file,"/Users/olivereielson/Desktop/saved_rac/"+base_file)
        copyfile("/Users/olivereielson/Desktop/man_edit/"+base_img,"/Users/olivereielson/Desktop/saved_rac/"+base_img)
        print(g)

def remove_extra():


    for g in glob.glob('/Users/olivereielson/Desktop/saved_rac/*.xml'):

        print(g)





remove_extra()


def xml_to_csv(path):

    classes_names = []
    xml_list = []
    for xml_file in glob.glob(path + "/*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        print(xml_file)
        for member in root.findall("object"):
            classes_names.append(member[0].text)
            print(len(member))
            value = (
                root.find("filename").text,
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text),
            )
            xml_list.append(value)
    column_name = [
        "filename",
        "width",
        "height",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    classes_names = list(set(classes_names))
    classes_names.sort()
    return xml_df, classes_names

#xml_to_csv("/Users/olivereielson/Desktop/new_data/")