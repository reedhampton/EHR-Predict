import csv
import os

dirpath = os.getcwd()
filename = dirpath + '/uploads/Patient Data.csv'

with open(filename, 'rb') as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')

    #Store the locations of the notes
    notes_begin = 19
    return_string = []
    found_doc = False
    found_event = False
    found_discharge = False
    
    #Retrieve the latest notes and store those
    for row in reversed(list(reader)):
        if found_doc and found_event and found_discharge:
            break

        if row[19] != '':
            return_string.append(row[19])
            found_doc = True
        
        if row[20] != '':
            return_string.append(row[20])
            found_event = True
            
        if row[21] != '':
            return_string.append(row[21])
            found_discharge = True
            
print (return_string)