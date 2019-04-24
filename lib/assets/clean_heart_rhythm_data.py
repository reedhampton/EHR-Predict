from tempfile import NamedTemporaryFile
import shutil
import csv

filename = '/home/ec2-user/environment/EHR-Predict/uploads/Patient Data.csv'
tempfile = NamedTemporaryFile(delete=False)

with open(filename, 'rt') as csvFile, tempfile:
	reader = csv.reader(csvFile, delimiter=',', quotechar='"')
	writer = csv.writer(tempfile, delimiter=',', quotechar='"')
    
    #Rhythm is the currently 14th column
	rows = []
	on_head_row = True
	rhythm_value_first = None
	rhythm_value_second = None
	rhythm_total_pos = 13
	at_end = False
	after_first_iteration = False
    #Determine the value we need to fill the beginning data cells with if they are null
	while not at_end :
		at_end = True
		rows = []
		if not after_first_iteration :
			for row in reader:
				if not on_head_row:
					if row[rhythm_total_pos] == '':
						rows.append(row)
						at_end = False
						continue
					else:
						rhythm_value_first = row[rhythm_total_pos]
						rows.append(row)
						at_end = False
						break
				on_head_row = False
				writer.writerow(row)

		for row in reader:
			if row[rhythm_total_pos] == '':
				rows.append(row)
				at_end = False
				continue
			else:
				rhythm_value_second = row[rhythm_total_pos]
				rows.append(row)
				at_end = False
				break
			
	#Write the rows that had a null entry
		count = 0
		median_index = (len(rows) / 2)
		for row in rows:
			count = count + 1
			if count <= median_index :
				row[rhythm_total_pos] = rhythm_value_first
			else :
				row[rhythm_total_pos] = rhythm_value_second
			writer.writerow(row)

		rhythm_value_first = rhythm_value_second
		after_first_iteration = True
#Write to our updated file CHANGE TO 'filename' WHEN OTHER SCRIPTS ARE DONE
shutil.move(tempfile.name, '/home/ec2-user/environment/EHR-Predict/uploads/Patient Data.csv')
