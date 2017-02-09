import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from savReaderWriter import SavReader

# Mortality Dataset
input_uuid_col = 0
is_dead_col = 4
death_date_col = 5
input_uuid_file = './csv/data_mortality_orig.csv'

print('[-] Loading Filter UUIDs from {} ...'.format(input_uuid_file))
uuids_to_filter = {}
dead_uuid_tracker = {}
max_death_date = datetime(1, 1, 1)
max_record_date = None
with open(input_uuid_file,
          mode='rt',
          errors='strict',
          encoding='utf-8') as uuidFile:
    reader = csv.reader(uuidFile, strict=True)
    headerRow = next(reader)

    for row in filter(lambda row: len(row) > 0, reader):
        uuid = str(row[input_uuid_col]).casefold()
        uuids_to_filter[uuid] = False
        if row[is_dead_col] == '1':
            dead_uuid_tracker[uuid] = False
            death_date = row[death_date_col].split('/')
            death_date = datetime(year=int(death_date[2]),
                                  month=int(death_date[1]),
                                  day=int(death_date[0]))
            if max_death_date < death_date:
                max_death_date = death_date

print('[-] Total UUIDs to find = {}'.format(len(uuids_to_filter)))
print('[-] Total Dead UUIDs to find = {}'.format(len(dead_uuid_tracker)))
print('[-] Maximum Death Date = {}'.format(max_death_date))
max_record_date = max_death_date - relativedelta(years=1)
print('[-] Maximum Record Date = {}'.format(max_record_date))


def transform_generator(uuid_map=uuids_to_filter):
    input_dir = './sav'
    outpur_dir = './filtered_csv'

    def uuid_filter(uuids):
        uuid_col = 0

        def filter(row):
            uuid = str(row[uuid_col], 'utf-8').casefold()
            return uuid in uuids
        return filter

    def date_recorded_filter(date_col):
        def filter(row):
            date_str = str(row[date_col], 'utf-8').split(' ')[0].split('-')
            record_date = datetime(year=int(date_str[0]),
                                   month=int(date_str[1]),
                                   day=int(date_str[2]))
            return record_date <= max_record_date
        return filter

    def category_filter(category_col, category):
        folded_cat = str(category).casefold()

        def filter(row):
            row_cat = str(row[category_col], 'utf-8').casefold()
            return row_cat == folded_cat
        return filter

    # create Transformation Descriptor
    transform_map = {
        'demographic': {
            'input_path': '{}/all_demographic.sav'.format(input_dir),
            'output_path': '{}/filtered_demographic.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map)]
        },
        'diagnoses': {
            'input_path': '{}/all_diagnoses.sav'.format(input_dir),
            'output_path': '{}/filtered_diagnoses.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map),
                        date_recorded_filter(date_col=1)]
        },
        'measures': {
            'input_path': '{}/all_measures.sav'.format(input_dir),
            'output_path': '{}/filtered_bmi.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map),
                        date_recorded_filter(date_col=3),
                        category_filter(category_col=1, category='bmi')]
        },
        'medical': {
            'input_path': '{}/all_medical.sav'.format(input_dir),
            'output_path': '{}/filtered_medical.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map),
                        date_recorded_filter(date_col=2)]
        },
        'pathology': {
            'input_path': '{}/all_pathology.sav'.format(input_dir),
            'output_path': '{}/filtered_egfr.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map),
                        date_recorded_filter(date_col=1),
                        category_filter(category_col=2, category='egfr')]
        },
        'prescriptions': {
            'input_path': '{}/all_prescriptions.sav'.format(input_dir),
            'output_path': '{}/filtered_prescriptions.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map)]
        },
        'snap': {
            'input_path': '{}/all_snap.sav'.format(input_dir),
            'output_path': '{}/filtered_snap.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map)]
        },
        'visits': {
            'input_path': '{}/all_visits.sav'.format(input_dir),
            'output_path': '{}/filtered_visits.csv'.format(outpur_dir),
            'filters': [uuid_filter(uuids=uuid_map)]
        },
    }

    for name, transform in transform_map.items():
        yield (name, transform)


for name, transform in transform_generator(uuid_map=uuids_to_filter):
    inputSavPath = transform.get('input_path')
    outputCsvPath = transform.get('output_path')

    print('[-] Filtering {} :: {} to {} ...'
          .format(name, inputSavPath, outputCsvPath))
    # Reset the stats collector
    for uuid in uuids_to_filter.keys():
        uuids_to_filter[uuid] = False
    for uuid in dead_uuid_tracker.keys():
        dead_uuid_tracker[uuid] = False

    total_rows = 0
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
                total_rows += 1
                if all([fn(row) for fn in transform.get('filters')]):
                    parsed_row = [field.decode()
                                  if type(field) is bytes else field
                                  for field in row]
                    outFilerWriter.writerow(parsed_row)

                    uuid = str(row[0], 'utf-8').casefold()
                    uuids_to_filter[uuid] = True
                    if uuid in dead_uuid_tracker:
                        dead_uuid_tracker[uuid] = True

    print('[v] Total rows in data file = {}'.format(total_rows))
    print('[v] UUIDs founds = {}'.format(sum(uuids_to_filter.values())))
    print('[v] Dead UUIDs found = {}'.format(sum(dead_uuid_tracker.values())))
