import csv
import glob
from os.path import basename, splitext
from savReaderWriter import SavReader

for inputSavPath in glob.glob('./sav/*.sav'):
    file_root = splitext(basename(inputSavPath))[0][4:]
    outputCsvPath = './csv/filtered_{}.csv'.format(file_root)
    print('Filtering {} to {} ...'.format(inputSavPath, outputCsvPath))

    # Reset the stats collector
    # for uuid in uuids_to_filter.keys():
    #     uuids_to_filter[uuid] = False

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

            print(header)
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