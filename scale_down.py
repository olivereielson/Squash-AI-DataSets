import glob
import cv2
import pandas as pd
import xml.etree.ElementTree as ET

scale=500
xml_list=[]


def resize(row):
    value = row.split(",")
    width = int(value[1])
    hight =int( value[2])

    xmin = int((int(value[4]) / width) * scale)
    ymin = int((int(value[5]) / hight) * scale)
    xmax = int((int(value[6]) / width) * scale)
    ymax = int((int(value[7]) / hight) * scale)

    img = cv2.imread("/Users/olivereielson/Desktop/new_data/"+value[0])
    img=cv2.resize(img,(scale,scale))
    cv2.imwrite("/Users/olivereielson/Desktop/scaled/"+value[0],img)
    revised_value=[value[0],scale,scale,value[3],xmin,ymin,xmax,ymax]
    xml_list.append(revised_value)






def two_scv(path):

    f = open(path, "r")
    csv_file=f.read().split("\n")

    length=len(csv_file)

    for idx,row in enumerate(csv_file):

        #print(str(idx)+"--"+str(length))
        print(idx/length)

        if not idx==0:
            resize(row)

        if idx>10:
            break





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

    xml_df.to_csv(path, index=None)



two_scv("OUTPUTS/test_labels.csv")
#two_scv("OUTPUTS/train_labels.csv")









