import csv

filename = "img2.csv"

last_row=""

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:

        if row[2] == "Squash" or row[2] == "Racquet":

            if row[1]==last_row:
                f = open("tfiles/" + name + ".txt", "a")
                f.write("\n"+row[3]+"-"+row[4]+"-"+row[7]+"-"+row[8]+"-"+row[2])
                f.close()
            else:
                print(row[1].replace("gs://","/Users/olivereielson/Desktop/dowload/"))
                name= row[1].replace("gs://sqaush/","").replace("gs://squash2/","")
                f = open("tfiles/"+name+".txt", "w")
                f.write(row[3]+"-"+row[4]+"-"+row[7]+"-"+row[8]+"-"+row[2])
                f.close()
                last_row=row[1]


