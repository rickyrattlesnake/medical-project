import csv
from savReaderWriter import SavReader

input_uuid_filename = './csv/ids_to_find.csv'
savFilename = './sav/all_patient_visits_2016.sav'
out_filename = './out/all_patient_visits_2016_filtered.csv'

ids_to_find = {}

with open(input_uuid_filename,
          mode='rt',
          errors='strict',
          encoding='utf-8') as uuidFile:
    reader = csv.reader(uuidFile,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    for row in reader:
        if len(row) >= 1:
            uuid = str(row[0]).casefold()
            ids_to_find[uuid] = 0

# print('ids to find \n {}'.format(ids_to_find))

with SavReader(savFilename) as reader:
    with open(out_filename,
              mode='wt',
              errors='strict',
              encoding='utf8') as outFile:
        outFilerWriter = csv.writer(outFile,
                                    delimiter=',',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL)
        header = [str(f, 'utf8').casefold() for f in reader.header]
        outFilerWriter.writerow(header)
        for row in reader:
            uuid = str(row[2], 'utf-8').casefold()
            if uuid in ids_to_find:
                ids_to_find[uuid] = 1
                row = [str(f, 'utf8') if type(f) is bytes else f for f in row]
                outFilerWriter.writerow(row)

# Print out numbers of how many were found and not found
num_total = 0
num_found = 0
num_not_found = 0
not_found_ids = []
for (id, found) in ids_to_find.items():
    if found:
        num_found += 1
    else:
        num_not_found += 1
        not_found_ids.append(id)
    num_total += 1


print('Results output - input_uuid_filename: {}, savFilename: {}, out_filename: {}'
      .format(input_uuid_filename, savFilename, out_filename))
print('Total input ids {} : found {}, not found {}'
      .format(num_total, num_found, num_not_found))
print('Ids not found : >> \n  {} \n >>'.format(not_found_ids))
