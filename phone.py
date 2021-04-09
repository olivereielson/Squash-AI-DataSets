import glob



phone = glob.glob('/Users/olivereielson/Desktop/phone/*.xml')

new_data = glob.glob('/Users/olivereielson/Desktop/new_data/*.xml')
f = open("not_phone.txt", "w")

for idx, file in enumerate(new_data):


    if not phone.__contains__(file.replace("/Users/olivereielson/Desktop/new_data/","/Users/olivereielson/Desktop/phone/")):

        f.write(file.replace("/Users/olivereielson/Desktop/new_data/","")+"\n")

f.close()