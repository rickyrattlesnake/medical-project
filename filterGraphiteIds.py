import csv
import glob
from os.path import basename, splitext
from savReaderWriter import SavReader

# Mortality Dataset
input_uuid_col = 0
input_uuid_file = './csv/data_mortality_orig.csv'

print('Loading Filter UUIDs from {} ...'.format(input_uuid_file))
uuids_to_filter = {}
with open(input_uuid_file,
          mode='rt',
          errors='strict',
          encoding='utf-8') as uuidFile:
    reader = csv.reader(uuidFile, strict=True)
    headerRow = next(reader)

    for row in reader:
        uuid = str(row[input_uuid_col]).casefold()
        uuids_to_filter[uuid] = False

for inputSavPath in glob.glob('./sav/*.sav'):
    file_root = splitext(basename(inputSavPath))[0][4:]
    outputCsvPath = './csv/filtered_{}.csv'.format(file_root)
    uuid_col = 0

    print('Filtering {} to {} ...'.format(inputSavPath, outputCsvPath))
    # Reset the stats collector
    for uuid in uuids_to_filter.keys():
        uuids_to_filter[uuid] = False

    total_uuids_in_data = 0
    with SavReader(inputSavPath) as savData:
        with open(outputCsvPath,
                  mode='wt',
                  errors='strict',
                  encoding='utf8') as outFile:
            outFilerWriter = csv.writer(outFile, strict=True)
            header = [str(field, 'utf8').casefold()
                      for field in savData.header]

            print(header)
            outFilerWriter.writerow(header)

            for row in savData:
                total_uuids_in_data += 1
                uuid = str(row[uuid_col], 'utf-8').casefold()
                if uuid in uuids_to_filter:
                    uuids_to_filter[uuid] = True
                    parsed_row = [field.decode()
                                  if type(field) is bytes else field
                                  for field in row]
                    outFilerWriter.writerow(parsed_row)

    print('Filtering statistics --- ')
    print('Total rows in data file = {}'.format(total_uuids_in_data))
    print('Total UUIDs to find = {}'.format(len(uuids_to_filter)))
    print('UUIDs founds = {}'.format(sum(uuids_to_filter.values())))
    # print('Ids not found >> [ {} ]'
    #       .format(','.join(uuid for (uuid, found) in uuids_to_filter.items()
    #                        if found)))
