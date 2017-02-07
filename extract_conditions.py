import csv
from diagnosis_classification import classify

uuid_pid_path = './csv/uuid_pid_map.csv'

uuid_pid_map = {}
pid_conditions = {}

print('[-] Collecting PID and UUID maps from {}'
      .format(uuid_pid_path))

with open(uuid_pid_path,
          mode='rt',
          errors='strict',
          encoding='utf-8') as uuid_pid_file:
    reader = csv.reader(uuid_pid_file, strict=True)
    headerRow = next(reader)

    for row in filter(lambda row: len(row) > 0, reader):
        uuid = str(row[0]).casefold()
        pid_hash = str(row[1]).casefold()

        if not pid_hash or not uuid:
            raise ValueError('PID or UUID is empty : row - {}'
                             .format(row))

        uuid_pid_map[uuid] = pid_hash
        pid_conditions[pid_hash] = []

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pid_conditions)))


def data_source_transformer():
    input_dir = './filtered_csv'

    transformers = {
        'medical': {
            'input_path': '{}/filtered_medical.csv'.format(input_dir),
            'uuid_col': 0,
            'condition_col': 1,
            'diagnosis_date_col': 2,
        },
        'diagnoses': {
            'input_path': '{}/filtered_diagnoses.csv'.format(input_dir),
            'uuid_col': 0,
            'condition_col': 2,
            'diagnosis_date_col': 1,
        }
    }

    for name, transformer in transformers.items():
        yield (name, transformer)


print('[-] Merging data sources ...')
for name, descriptor in data_source_transformer():
    with open(descriptor['input_path'],
              mode='rt',
              errors='strict',
              encoding='utf-8') as sourceFile:
        reader = csv.reader(sourceFile, strict=True)
        headerRow = next(reader)

        for row in filter(lambda row: len(row) > 0, reader):
            condition = str(row[descriptor['condition_col']])
            diag_date = str(row[descriptor['diagnosis_date_col']])
            diag_date = diag_date.split(' ')[0]

            uuid = str(row[descriptor['uuid_col']]).casefold()
            if uuid not in uuid_pid_map:
                raise ValueError('UUID not in uuid_pid map - ' + uuid)

            pid = uuid_pid_map[uuid].casefold()
            if pid not in pid_conditions:
                raise ValueError('PID not in pid_conditions - ' + pid)

            classified_conditions = classify(condition)
            classified_conditions['pid_hash'] = pid
            classified_conditions['condition'] = condition
            classified_conditions['diagnosis_date'] = diag_date

            pid_conditions[pid].append(classified_conditions)

output_path = './extracted_csv/pid_conditions.csv'
print('[-] Writing pid_conditions to {}'
      .format(output_path))

with open(output_path,
          mode='wt',
          errors='strict',
          encoding='utf-8') as outFile:
        writer = csv.writer(outFile, strict=True)
        header = [
            'pid_hash',
            'condition',
            'diagnosis_date',
            'cancer',
            'metastatic_disease',
            'chemotherapy',
            'radiotherapy',
            'dementia',
            'chronic_heart_failure',
            'copd',
            'chronic_renal_failure',
            'stage_4_or_5_renal_failure',
            'dialysis',
            'chronic_liver_failure',
        ]
        writer.writerow(header)

        for pid_hash, conditions in pid_conditions.items():
            for condition in conditions:
                writer.writerow([
                    pid_hash,
                    condition['condition'],
                    condition['diagnosis_date'],
                    condition['cancer'],
                    condition['metastatic_disease'],
                    condition['chemotherapy'],
                    condition['radiotherapy'],
                    condition['dementia'],
                    condition['chronic_heart_failure'],
                    condition['copd'],
                    condition['chronic_renal_failure'],
                    condition['stage_4_or_5_renal_failure'],
                    condition['dialysis'],
                    condition['chronic_liver_failure'],
                ])
