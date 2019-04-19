from tempfile import NamedTemporaryFile
import shutil
import csv

filename = '../../app/assets/data/demo_data.csv'
tempfile = NamedTemporaryFile(delete=False)

with open(filename, 'rb') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    
    #GCS_Total is the currently 16th column
    rows = []
    skip_head_row = True
    copied_gcs_value = None
    skip_rows = 0
    
    #Determine the value we need to fill the beginning data cells with
    for row in reader:
        skip_rows = skip_rows + 1
        if not skip_head_row:
            if row[15] == '':
                rows.append(row)
                continue
            else:
                copied_gcs_value = row[15]
                rows.append(row)
                break
        skip_head_row = False
        writer.writerow(row)
    
    #Write the first rows that had a null entry
    for row in rows:
        row[15] = copied_gcs_value
        writer.writerow(row)
            
    #Keep reading and writing
    for row in reader:
        if row[15] == '':
            row[15] = copied_gcs_value
        else:
            copied_gcs_value = row[15]
        writer.writerow(row)


#Write to our updated file
shutil.move(tempfile.name, '../../app/assets/data/sample_data.csv')
