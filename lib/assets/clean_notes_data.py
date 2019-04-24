from tempfile import NamedTemporaryFile
import shutil
import csv
import os

dirpath = os.getcwd()
filename = dirpath + '/uploads/Patient Data.csv'
tempfile = NamedTemporaryFile(delete=False)

with open(filename, 'rb') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    
    #Store the locations of the notes
    beginning = 0
    notes_begin = 19
    
    #Determine the value we need to fill the beginning data cells with if they are null
    for row in reader:
        writer.writerow(row[beginning:notes_begin])

#Write to our updated file CHANGE TO 'filename' WHEN OTHER SCRIPTS ARE DONE
shutil.move(tempfile.name, dirpath + '/uploads/Patient Data.csv')
