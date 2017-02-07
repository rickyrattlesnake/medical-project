import csv
from load_pid_maps import load_pid_uuid_maps
from utils import convert_to_int

pids, uuid_pid_map = load_pid_uuid_maps()

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pids)))

input_path = './filtered_csv/filtered_snap.csv'
output_path = './extracted_csv/pid_snap.csv'

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
            'smoker',
            'smokes_per_day',
            'alcohol_consumption',
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
                'smoker': str(row['smoker'].strip()),
                'smokes_per_day': convert_to_int(row['smokes_per_day']),
                'alcohol_consumption': convert_to_int(row['alcohol_consumption']),
            })
