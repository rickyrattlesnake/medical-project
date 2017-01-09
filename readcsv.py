import csv

input_uuid_filename = ''
filename = 'top_10_all.csv'

with open(filename,
          mode='rt',
          errors='strict',
          encoding='utf-8') as csvFile:
    reader = csv.reader(csvFile,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    for row in reader:
        if len(row) >= 2:
            print(row[2])
