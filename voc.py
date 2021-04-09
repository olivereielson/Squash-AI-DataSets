from pascal_voc_writer import Writer
from PIL import Image
import glob
from shutil import copyfile

Globs = glob.glob("/Users/olivereielson/PycharmProjects/datasets/tfiles/*.txt")

for file in Globs:


        image = Image.open("/Users/olivereielson/Desktop/dowload/" + file[53:-4])
        copyfile("/Users/olivereielson/Desktop/dowload/" + file[53:-4], "/Users/olivereielson/PycharmProjects/datasets/voc_outputs/" + file[53:-4])
        width, height = image.size




        writer = Writer("/Users/olivereielson/Desktop/dowload/" + file[53:-4], width, height)
        f = open(file, "r")
        t = f.read().split("\n")
        for line in t:
            points = line.split("-")
            #print(points)
            writer.addObject(points[4], int(float(points[0]) * width), int(float(points[1]) * height), int(float(points[2]) * width),  int(float(points[3]) * height))

        writer.save(
            "/Users/olivereielson/PycharmProjects/datasets/voc_outputs/" + file[53:-4].replace(".jpg", ".xml").replace(  ".JPG", ".xml"))
