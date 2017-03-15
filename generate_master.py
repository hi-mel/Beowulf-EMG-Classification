# csv reader reads each file in dir, takes middle 80% of data, merges into master csv, writes to file

import os
import csv

master_file_name = 'master_training_data.csv'

if (os.path.exists(master_file_name)):
    os.remove(master_file_name)

csv_files = [name for name in os.listdir('.') if name.lower().endswith('.csv')]

master_data = []

for csv_file in csv_files:
    f = open(csv_file, 'r')
    reader = csv.reader(f)
    
    contents = list(reader)
    num_rows = len(contents)

    for row in contents[int(0.1*num_rows):int(0.9*num_rows)]:
        master_data.append(row)

    f.close()

f = open(master_file_name, 'w+')
writer = csv.writer(f)

for row in master_data:
    writer.writerow(row)

f.close()
