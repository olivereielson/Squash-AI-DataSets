import glob

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from pascal_voc_writer import Writer

from data_generator_object_detection_2d.bounding_box_utils.bounding_box_utils import iou

from data_generator_object_detection_2d.object_detection_2d_data_generator import DataGenerator
from data_generator_object_detection_2d.transformations.object_detection_2d_patch_sampling_ops import *
from data_generator_object_detection_2d.transformations.object_detection_2d_geometric_ops import *
from data_generator_object_detection_2d.transformations.object_detection_2d_photometric_ops import *
from data_generator_object_detection_2d.transformations.object_detection_2d_image_boxes_validation_utils import *
from data_generator_object_detection_2d.data_augmentation_chains.data_augmentation_chain_original_ssd import *


def random_color():
    return (random.randint(1, 256), random.randint(1, 256), random.randint(1, 256)),


g = open("image_list.txt", "w")
g.write("")
g.close()

Globs = glob.glob("/Users/olivereielson/PycharmProjects/datasets/voc_outputs/*.jpg")
f = open("image_list.txt", "a")
for g in Globs:
    f.write(g[0:-4] + "\n")
f.close()

images_dir = 'voc_outputs/'
annotations_dir = 'voc_outputs/'
image_set_filename = 'image_list.txt'

dataset = DataGenerator(labels_output_format=('class_id', 'xmin', 'ymin', 'xmax', 'ymax'))

# The XML parser needs to now what object class names to look for and in which order to map them to integers.
classes = ['Squash', 'Racquet']

dataset.parse_xml(images_dirs=[images_dir],
                  image_set_filenames=[image_set_filename],
                  annotations_dirs=[annotations_dir],
                  classes=classes,
                  include_classes='all',
                  exclude_truncated=False,
                  exclude_difficult=False,
                  ret=False)

image_validator = ImageValidator(overlap_criterion='area',
                                 bounds=(0.3, 1.0),
                                 n_boxes_min=1)

box_filter = BoxFilter(overlap_criterion='area',
                       overlap_bounds=(0.4, 1.0))

# Utility transformations
convert_to_3_channels = ConvertTo3Channels()  # Make sure all images end up having 3 channels.
convert_RGB_to_HSV = ConvertColor(current='RGB', to='HSV')
convert_HSV_to_RGB = ConvertColor(current='HSV', to='RGB')
convert_to_float32 = ConvertDataType(to='float32')
convert_to_uint8 = ConvertDataType(to='uint8')
resize = Resize(height=500, width=500)

# Photometric transformations
random_brightness = RandomBrightness(lower=-48, upper=48, prob=0.5)
random_contrast = RandomContrast(lower=0.5, upper=1.5, prob=0.5)
random_saturation = RandomSaturation(lower=0.5, upper=1.5, prob=0.5)
random_hue = RandomHue(max_delta=18, prob=0.5)

# Geometric transformations
random_flip = RandomFlip(dim='horizontal', prob=0.9)
random_flip1 = RandomFlip(dim='vertical', prob=0.9)
random_translate = RandomTranslate(image_validator=image_validator, box_filter=box_filter, background=random_color())

patch_coord_generator = PatchCoordinateGenerator(must_match='w_ar',
                                                 min_scale=0.3,
                                                 max_scale=2.0,
                                                 scale_uniformly=False,
                                                 min_aspect_ratio=0.5,
                                                 max_aspect_ratio=2.0)
random_patch = RandomPatch(patch_coord_generator=patch_coord_generator,
                           box_filter=box_filter,
                           image_validator=image_validator,
                           n_trials_max=10,
                           clip_boxes=False,
                           prob=5.0,
                           can_fail=False,
                           background=random_color())

random_rotate = RandomRotate(prob=0.99)

# Define the processing chain

data_augmentation = [convert_to_3_channels,
                     convert_to_float32,
                     random_brightness,
                     random_contrast,
                     convert_to_uint8,
                     convert_RGB_to_HSV,
                     convert_to_float32,
                     random_saturation,
                     random_hue,
                     convert_to_uint8,
                     convert_HSV_to_RGB,
                     random_patch,
                     random_flip,
                     resize,
                     random_rotate,
                     random_flip1,
                     ]

data_augmentation2 = [convert_to_3_channels,
                      convert_to_float32,
                      random_brightness,
                      random_contrast,
                      convert_to_uint8,
                      convert_RGB_to_HSV,
                      convert_to_float32,
                      random_saturation,
                      random_hue,
                      convert_to_uint8,
                      convert_HSV_to_RGB,
                      random_flip,
                      random_rotate,
                      ]

batch_size = 100

data_generator = dataset.generate(batch_size=batch_size,
                                  shuffle=True,
                                  transformations=data_augmentation2,
                                  label_encoder=None,
                                  returns={'processed_images',
                                           'processed_labels',
                                           'filenames',
                                           'original_images',
                                           'original_labels'},
                                  keep_images_without_gt=False)

processed_images, processed_annotations, filenames, original_images, original_annotations = next(data_generator)

# print(processed_annotations[0])

for idx, img in enumerate(processed_images):
    img_name = "test/" + str(idx) + filenames[idx][58:]
    plt.imsave(img_name, img)
    image = Image.open(img_name)
    width, height = image.size

    writer = Writer(img_name, width, height)

    for an in processed_annotations[idx]:
        # print(an)
        if str(an).__contains__("-"):
            print(an)
        elif height < an[4] or width < an[3]:
            print("why")
            print(an)


        elif an[3] - an[1] > 8 and an[4] - an[2] > 8:
            writer.addObject(classes[an[0]], an[1], an[2], an[3], an[4])
        else:
            print(an)

    writer.save("test/" + str(idx) + filenames[idx][58:-4] + ".xml")

# print(processed_images[0])
for i in range(5):

    fig, cell = plt.subplots(1, 2, figsize=(20, 16), )
    cell[0].imshow(original_images[i])
    cell[1].imshow(processed_images[i])

    for box in original_annotations[i]:
        xmin = box[1]
        ymin = box[2]
        xmax = box[3]
        ymax = box[4]
        # color = 0.3,0.3,0.5,
        label = '{}'.format(classes[int(box[0])])
        cell[0].add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, color='black', fill=False, linewidth=2))
        cell[0].text(xmin, ymin, label, size='x-large', color='white', bbox={'facecolor': "black", 'alpha': 1.0})

    for box in processed_annotations[i]:
        xmin = box[1]
        ymin = box[2]
        xmax = box[3]
        ymax = box[4]
        color = "black"
        label = '{}'.format(classes[int(box[0])])
        cell[1].add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, color=color, fill=False, linewidth=2))
        cell[1].text(xmin, ymin, label, size='x-large', color='white', bbox={'facecolor': color, 'alpha': 1.0})

    plt.pause(1)

from distutils.dir_util import copy_tree

# copy subdirectory example
fromDirectory = "test"
toDirectory = "allfiles"

copy_tree(fromDirectory, toDirectory)

import shutil

shutil.rmtree('test')
import os

os.makedirs('test')
