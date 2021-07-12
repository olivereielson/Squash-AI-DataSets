import shutil
import glob
from progress.bar import Bar


bar = Bar('Moving Files', fill='|', suffix='%(percent).1f%% - %(eta)ds  ', max=len(glob.glob("/Users/olivereielson/Desktop/check_over/*")))

for file in glob.glob("/Users/olivereielson/Desktop/check_over/*"):


    dst = "/Volumes/Extra_Storage/new_data/" + file.split("/")[-1]

    shutil.copy(file, dst)
    bar.next()

bar.finish()