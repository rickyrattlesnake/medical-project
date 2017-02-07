import csv
import glob
from os.path import basename, splitext


def merge_fields(delimiter, fields, validator=lambda x: True):
    # convert to string and concatenate
    if not validator(fields):
        raise ValueError('Merge Failed with invalid Fields - {}'
                         .format(fields))
    return delimiter.join(str(field) for field in fields)


def unmergeField(delimiter, merged_field):
    return merged_field.split(delimiter)


def filtered_to_merged_paths():
    for inputFilteredCsv in glob.glob('./csv/filtered_*.csv'):
        file_root = splitext(basename(inputFilteredCsv))[0][9:]
        outputMergedCsv = './merged_csv/merged_{}.csv'.format(file_root)
        yield (inputFilteredCsv, outputMergedCsv)


uuid_col = 0
merge_delimiter = '||'

for (inputPath, outputPath) in filtered_to_merged_paths():

    print('----- Merging {} to {} ...'.format(inputPath, outputPath))

    uuid_to_fields = {}

    total_rows = 0
    header = ''
    with open(inputPath,
              mode='rt',
              errors='strict',
              encoding='utf8') as inFile:
        unmergedCsv = csv.reader(inFile, strict=True)
        header = next(unmergedCsv)

        for row in filter(lambda row: len(row) > 0, unmergedCsv):
            uuid = row[uuid_col]
            unmerged_fields = [f for i, f in enumerate(row) if i != uuid_col]
            # Expect the fields to be in the same order to merge
            # output should be in same order to write
            if uuid in uuid_to_fields:
                existing_fields = uuid_to_fields[uuid]
                merged_fields = [merge_fields(merge_delimiter, [x, y])
                                 for x, y in zip(existing_fields,
                                                 unmerged_fields)]
                uuid_to_fields[uuid] = merged_fields
            else:
                uuid_to_fields[uuid] = unmerged_fields

            total_rows += 1

    with open(outputPath,
              mode='wt',
              errors='strict',
              encoding='utf8') as outFile:
            mergedCsv = csv.writer(outFile, strict=True)
            mergedCsv.writerow(header)

            for (uuid, fields) in uuid_to_fields.items():
                mergedCsv.writerow(fields[:uuid_col] +
                                   [uuid] +
                                   fields[uuid_col:])

    print('Total rows in data file = {}'.format(total_rows))
    print('Total unique UUIDs = {}'.format(len(uuid_to_fields)))
    print('----- End Merging Results -----')
