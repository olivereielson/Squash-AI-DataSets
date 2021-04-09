
import tensorflow as tf

#raw_dataset = tf.data.TFRecordDataset("OUTPUTS/test.record")

#for raw_record in raw_dataset.take(1):
    #example = tf.train.Example()
    #example.ParseFromString(raw_record.numpy())
    #print(example)
from progress.bar import Bar

bar = Bar('Loading', fill='|', suffix='%(percent)d%%', max=1000)

for i in range(1000):
    bar.next()

bar.finish()

with Bar('Processing', max=20) as bar:
    for i in range(20):
        # Do some work
        bar.next()