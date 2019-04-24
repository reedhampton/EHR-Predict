from tempfile import NamedTemporaryFile
import shutil
import csv

import os

dirpath = os.getcwd()

filename = dirpath + '/uploads/Patient Data.csv'
tempfile = NamedTemporaryFile(delete=False)

with open(filename, 'rt') as csvFile, tempfile:
	reader = csv.reader(csvFile, delimiter=',', quotechar='"')
	writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    

	rows = []
	on_head_row = True
	hr_value_first = None
	hr_value_second = None
	hr_total_pos = 12
	at_end = False
	after_first_iteration = False
    #Determine the value we need to fill the beginning data cells with if they are null
	while not at_end :
		at_end = True
		rows = []
		if not after_first_iteration :
			for row in reader:
				if not on_head_row:
					if row[hr_total_pos] == '':
						rows.append(row)
						at_end = False
						continue
					else:
						hr_value_first = row[hr_total_pos]
						rows.append(row)
						at_end = False
						break
				on_head_row = False
				writer.writerow(row)

		for row in reader:
			if row[hr_total_pos] == '':
				rows.append(row)
				at_end = False
				continue
			else:
				hr_value_second = row[hr_total_pos]
				rows.append(row)
				at_end = False
				break
			
	#Write the rows that had a null entry
		count = 0
		inc_value = (float(hr_value_first))
		dif = float(hr_value_second) - float(hr_value_first)
		if len(rows) > 0 :
			slope =  dif / float(len(rows))
			for row in rows:
				count = count + 1
				if row[hr_total_pos] == '':
					if inc_value < 0:
						row[hr_total_pos] = 0
					else :
						row[hr_total_pos] = int(inc_value)
					inc_value = inc_value + slope
				elif count > 1 or len(rows) == 1:
					row[hr_total_pos] = hr_value_second
				else :
					row[hr_total_pos] = hr_value_first
				writer.writerow(row)
		
		hr_value_first = hr_value_second
		after_first_iteration = True
#Write to our updated file CHANGE TO 'filename' WHEN OTHER SCRIPTS ARE DONE
shutil.move(tempfile.name, dirpath + '/uploads/Patient Data.csv')
