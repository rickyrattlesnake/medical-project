import csv
from load_pid_maps import load_pid_uuid_maps
from utils import convert_to_date

pids, uuid_pid_map = load_pid_uuid_maps()

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pids)))

input_path = './filtered_csv/filtered_prescriptions.csv'
output_path = './extracted_csv/pid_prescriptions.csv'

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
            'reason',
            'trade_name',
            'ther_class',
            'script_date',
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
                'reason': str(row['reason']),
                'trade_name': str(row['trade_name']),
                'ther_class': str(row['therclass']),
                'script_date': convert_to_date(row['script_date']),
            })
