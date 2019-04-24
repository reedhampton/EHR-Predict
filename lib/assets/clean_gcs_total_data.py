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
    
    #GCS_Total is the currently 16th column
    rows = []
    on_head_row = True
    gcs_value = None
    gcs_total_pos = 15
    
    #Determine the value we need to fill the beginning data cells with if they are null
    for row in reader:
        if not on_head_row:
            if row[gcs_total_pos] == '':
                rows.append(row)
                continue
            else:
                gcs_value = row[gcs_total_pos]
                rows.append(row)
                break
        on_head_row = False
        writer.writerow(row)
    
    #Write the first rows that had a null entry
    for row in rows:
        row[gcs_total_pos] = gcs_value
        writer.writerow(row)
            
    #Keep reading and writing and updating each row as needed
    for row in reader:
        if row[gcs_total_pos] == '':
            row[gcs_total_pos] = gcs_value
        else:
            gcs_value = row[gcs_total_pos]
        writer.writerow(row)

#Write to our updated file CHANGE TO 'filename' WHEN OTHER SCRIPTS ARE DONE
shutil.move(tempfile.name, dirpath + '/uploads/Patient Data.csv')
