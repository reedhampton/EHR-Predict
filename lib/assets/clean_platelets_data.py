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
	p_value_first = None
	p_value_second = None
	p_total_pos = 16
	at_end = False
	after_first_iteration = False
    #Determine the value we need to fill the beginning data cells with if they are null
	while not at_end :
		at_end = True
		rows = []
		##########################################################
		#FIRST ITERATION
		if not after_first_iteration :
			for row in reader:
				if not on_head_row:
					if row[p_total_pos] == '':
						rows.append(row)
						at_end = False
						continue
					else:
						p_value_first = row[p_total_pos]
						rows.append(row)
						at_end = False
						break
				on_head_row = False
				writer.writerow(row)
		##############################################################
		
		# ALL OTHER ITERATIONS
		for row in reader:
			if row[p_total_pos] == '':
				rows.append(row)
				at_end = False
				continue
			else:
				p_value_second = row[p_total_pos]
				rows.append(row)
				at_end = False
				break
			
	#Write the rows that had a null entry
		count = 0
		inc_value = (float(p_value_first))
		dif = float(p_value_second) - float(p_value_first)
		if len(rows) > 0 :
			slope =  dif / float(len(rows))
			
			for row in rows:
				count = count + 1
				if row[p_total_pos] == '':
					if inc_value < 0:
						row[p_total_pos] = 0
					else :
						row[p_total_pos] = int(inc_value)
					inc_value = inc_value + slope
					
				elif count == 1 or len(rows) > 1:
					row[p_total_pos] = p_value_first
					
				else :
					row[p_total_pos] = p_value_second
				writer.writerow(row)
		
		p_value_first = p_value_second
		after_first_iteration = True
#Write to our updated file CHANGE TO 'filename' WHEN OTHER SCRIPTS ARE DONE
shutil.move(tempfile.name, '/home/ec2-user/environment/EHR-Predict/uploads/Patient Data.csv')
