import csv
import re
from load_pid_maps import load_pid_uuid_maps

pids, uuid_pid_map = load_pid_uuid_maps()

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pids)))


def convert_egfr_score(in_value):
    score = str(in_value).strip()
    if re.match(r'>.?90', score):
        return 91.0
    elif re.match(r'<.?10', score):
        return 9.0
    else:
        return float(score)


input_path = './filtered_csv/filtered_egfr.csv'
output_path = './extracted_csv/pid_egfr.csv'

with open(input_path,
          mode='rt',
          errors='strict',
          encoding='utf-8') as source_file:
    reader = csv.DictReader(source_file, strict=True)

    with open(output_path,
              mode='wt',
              errors='strict',
              encoding='utf-8') as out_file:
        out_fieldnames = [
            'pid_hash',
            'egfr_measurement',
            'egfr_measurement_date',
        ]
        writer = csv.DictWriter(out_file,
                                fieldnames=out_fieldnames,
                                extrasaction='raise')
        writer.writeheader()

        for row in filter(lambda row: len(row) > 0, reader):
            uuid = str(row['patient_uuid']).casefold()

            if uuid not in uuid_pid_map:
                raise ValueError('UUID not found in UUID_PID_MAP - {}'
                                 .format(uuid))

            writer.writerow({
                'pid_hash': uuid_pid_map[uuid],
                'egfr_measurement': convert_egfr_score(row['result']),
                'egfr_measurement_date': str(row['result_date']).split(' ')[0],
            })
