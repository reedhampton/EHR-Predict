from tempfile import NamedTemporaryFile
import shutil
import csv
import re

filename = '../../app/assets/data/demo_table_w_weight.csv'
tempfile = NamedTemporaryFile(delete=False)

#Global variables
rows = []
on_head_row = True
cr_pos = 17
first_cr = None

def main():
    with open(filename, 'rb') as csvFile, tempfile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        writer = csv.writer(tempfile, delimiter=',', quotechar='"')
        
        #Determine the value we need to fill the beginning data cells with if they are null
        global on_head_row
        global first_cr
        for row in reader:
            if not on_head_row:
                if row[cr_pos] == '':
                    rows.append(row)
                    continue
                else:
                    first_cr = float(row[cr_pos])
                    rows.append(row)
                    break
            on_head_row = False
            writer.writerow(row)
        
        #Write the first rows that had a null entry
        for row in rows:
            row[cr_pos] = first_cr
            writer.writerow(row)
            
        #Clear the rows list
        del rows[:]
                
        second_cr = None
        current_cr = None;
        for row in reader:
            if row[cr_pos] == '':
                rows.append(row)
                continue
            else:
                if len(rows) != 0:
                    #get the second cr_value and calculate rate of change
                    current_cr = first_cr
                    second_cr = row[cr_pos]
                    rate_of_change = (float(second_cr) - float(first_cr)) / len(rows)
                    #go and edit our rows
                    for row_to_change in rows:
                        row_to_change[cr_pos] = float(current_cr) - rate_of_change
                        current_cr = row_to_change[cr_pos]
                        writer.writerow(row_to_change)
                    del rows[:]
                    first_cr = second_cr
            #Write the row we just saw
            writer.writerow(row)

    #Write to our updated file CHANGE TO 'filename' WHEN OTHER SCRIPTS ARE DONE
    shutil.move(tempfile.name, filename)

if __name__== '__main__':
    main()