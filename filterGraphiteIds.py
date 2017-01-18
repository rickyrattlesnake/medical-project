import csv
from savReaderWriter import SavReader

# Mortality Dataset
input_uuid_col = 0
input_uuid_filename = './csv/ids_to_find.csv'

# Filter Mappings { input_sav => filtered_output.csv }
uuid_col = 2
filter_file_map = {
    './sav/all_past_medical_history_2016.sav': './out/all_past_medical_history_2016_filtered.csv',
    './sav/all_diagnoses_2016.sav': './out/all_diagnoses_2016_filtered.csv'
}
# savFilename = './sav/all_past_medical_history_2016.sav'
# out_filename = './out/all_past_medical_history_2016_filtered.csv'

uuids_to_filter = {}
print('Loading Filter UUIDs from {} ...'.format(input_uuid_filename))
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
            uuid = str(row[input_uuid_col]).casefold()
            uuids_to_filter[uuid] = False


for (inputSavPath, outputCsvPath) in filter_file_map.items():
    print('Filtering {} to {} ...'.format(inputSavPath, outputCsvPath))

    # Reset the stats collector
    for uuid in uuids_to_filter.keys():
        uuids_to_filter[uuid] = False

    with SavReader(inputSavPath) as savData:
        with open(outputCsvPath,
                  mode='wt',
                  errors='strict',
                  encoding='utf8') as outFile:
            outFilerWriter = csv.writer(outFile,
                                        delimiter=',',
                                        quotechar='|',
                                        quoting=csv.QUOTE_MINIMAL)
            header = [str(field, 'utf8').casefold()
                      for field in savData.header]
            outFilerWriter.writerow(header)

            for row in savData:
                uuid = str(row[uuid_col], 'utf-8').casefold()
                if uuid in uuids_to_filter:
                    uuids_to_filter[uuid] = True
                    parsed_row = [str(field, 'utf8')
                                  if type(field) is bytes else field
                                  for field in row]
                    outFilerWriter.writerow(parsed_row)

    print('Filtering statistics --- ')
    print('Total UUIDs to Filter = {}'.format(len(uuids_to_filter)))
    print('UUIDs filtered = {}'.format(sum(uuids_to_filter.values())))
    # print('Ids not found >> [ {} ]'
    #       .format(','.join(uuid for (uuid, found) in uuids_to_filter.items()
    #                        if found)))
