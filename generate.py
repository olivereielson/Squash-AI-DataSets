"""
Usage:

# Create train data:
python generate_tfrecord.py --label=<LABEL> --csv_input=<PATH_TO_ANNOTATIONS_FOLDER>/train_labels.csv  --output_path=<PATH_TO_ANNOTATIONS_FOLDER>/train.record <PATH_TO_ANNOTATIONS_FOLDER>/label_map.pbtxt

# Create test data:
python generate_tfrecord.py --label=<LABEL> --csv_input=<PATH_TO_ANNOTATIONS_FOLDER>/test_labels.csv  --output_path=<PATH_TO_ANNOTATIONS_FOLDER>/test.record  --label_map <PATH_TO_ANNOTATIONS_FOLDER>/label_map.pbtxt
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from progress.bar import Bar

import os
import io

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import sys

from tensorflow.python.ops.image_ops_impl import ResizeMethodV1

sys.path.append("models/research")

from PIL import Image
from models.research.object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.compat.v1.flags
flags.DEFINE_string("csv_input", "", "Path to the CSV input")
flags.DEFINE_string("output_path", "", "Path to output TFRecord")
flags.DEFINE_string("img_path", "", "Path to images")

flags.DEFINE_string(
    "label_map",
    "",
    "Path to the `label_map.pbtxt` contains the <class_name>:<class_index> pairs generated by `xml_to_csv.py` or manually.",
)
# if your image has more labels input them as
# flags.DEFINE_string('label0', '', 'Name of class[0] label')
# flags.DEFINE_string('label1', '', 'Name of class[1] label')
# and so on.
FLAGS = flags.FLAGS


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def split(df, group):
    data = namedtuple("data", ["filename", "object"])
    gb = df.groupby(group)
    return [
        data(filename, gb.get_group(x))
        for filename, x in zip(gb.groups.keys(), gb.groups)
    ]


def load_image(addr):
    # save resized images for faster proccesing
    f_name = addr.split("/")[-1]

    if not os.path.exists("/Users/olivereielson/Desktop/small_image/" + f_name):

        img = cv2.imread(addr)
        img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("/Users/olivereielson/Desktop/small_image/" + f_name, img)
        # print("saved new image")
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_image_string = cv2.imencode('.jpg', img)[1].tostring()
        return encoded_image_string
    else:
        img = cv2.imread("/Users/olivereielson/Desktop/small_image/" + f_name)
        encoded_image_string = cv2.imencode('.jpg', img)[1].tostring()
        return encoded_image_string


def create_tf_example(group, path, label_map):
    path = os.path.join(FLAGS.img_path, "{}".format(group.filename))

    img = load_image(path)

    # image = Image.open(path)
    # width, height = image.size

    filename = group.filename.encode("utf8")
    image_format = b"jpg"
    # check if the image format is matching with your images.
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        # xmins.append(row["xmin"] / width)
        # xmaxs.append(row["xmax"] / width)
        # ymins.append(row["ymin"] / height)
        # ymaxs.append(row["ymax"] / height)
        xmins.append(row["xmin"] / row["width"])
        xmaxs.append(row["xmax"] / row["width"])
        ymins.append(row["ymin"] / row["height"])
        ymaxs.append(row["ymax"] / row["height"])

        classes_text.append(row["class"].encode("utf8"))
        class_index = label_map.get(row["class"])
        assert (
                class_index is not None
        ), "class label: `{}` not found in label_map: {}".format(
            row["class"], label_map
        )
        classes.append(class_index)

    tf_example = tf.train.Example(
        features=tf.train.Features(
            feature={
                "image/height": dataset_util.int64_feature(640),
                "image/width": dataset_util.int64_feature(640),
                "image/filename": dataset_util.bytes_feature(filename),
                "image/source_id": dataset_util.bytes_feature(filename),
                "image/encoded": _bytes_feature(img),
                "image/format": dataset_util.bytes_feature(image_format),
                "image/object/bbox/xmin": dataset_util.float_list_feature(xmins),
                "image/object/bbox/xmax": dataset_util.float_list_feature(xmaxs),
                "image/object/bbox/ymin": dataset_util.float_list_feature(ymins),
                "image/object/bbox/ymax": dataset_util.float_list_feature(ymaxs),
                "image/object/class/text": dataset_util.bytes_list_feature(
                    classes_text
                ),
                "image/object/class/label": dataset_util.int64_list_feature(classes),
            }
        )
    )
    return tf_example


def main(_):
    writer = tf.compat.v1.python_io.TFRecordWriter(FLAGS.output_path)
    # print("hee"+str(FLAGS.img_path))

    path = os.path.join(os.getcwd(), FLAGS.img_path)
    examples = pd.read_csv(FLAGS.csv_input)

    # Load the `label_map` from pbtxt file.
    from models.research.object_detection.utils import label_map_util

    label_map = label_map_util.load_labelmap(FLAGS.label_map)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True
    )
    category_index = label_map_util.create_category_index(categories)
    label_map = {}
    for k, v in category_index.items():
        label_map[v.get("name")] = v.get("id")

    grouped = split(examples, "filename")

    legnth = len(grouped)

    bar = Bar('creating tfrecord', fill='|', suffix='%(percent).1f%% - %(eta)ds  ', max=legnth)

    for group in grouped:
        tf_example = create_tf_example(group, path, label_map)
        writer.write(tf_example.SerializeToString())
        bar.next()

    bar.finish()

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print("Successfully created the TFRecords: {}".format(output_path))


if __name__ == "__main__":
    tf.compat.v1.app.run()