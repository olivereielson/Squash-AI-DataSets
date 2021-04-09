import csv
from PIL import Image
import os



filename = ["OUTPUTS/test_labels.csv","OUTPUTS/train_labels.csv"]

for f in filename:
    with open(f, 'r') as csvfile:
        csvreader = csv.reader(csvfile)



        for row in csvreader:




            try:




                if str(row[1:7]).__contains__("-"):
                    print("he")

                if float(row[6])-float(row[4])<8:
                    #os.remove('voc_outputs/' + row[0])
                    print("he")
                    print(row)

                if float(row[7]) - float(row[5]) <8:
                    #os.remove('voc_outputs/' + row[0])
                    print("he")
                    print(row)

                    print("hew")


                if float(row[6])> float(row[1]):
                    print(row)
                    print(str(row[6])+"   one    "+str(row[1]))

                    #os.remove('voc_outputs/' + row[0])

                if float(row[7]) > float(row[2]):
                    print(row)


                    #os.remove('voc_outputs/' + row[0])


            except:
                print(row)



