import csv
from load_pid_maps import load_pid_uuid_maps
from utils import convert_to_int, convert_to_date, convert_to_bool_int

pids, uuid_pid_map = load_pid_uuid_maps()

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pids)))

input_path = './filtered_csv/filtered_visits.csv'
output_path = './extracted_csv/pid_visits.csv'

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
            'visit_date',
            'nonvisit',
            'cancelled',
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
                'visit_date': convert_to_date(row['visitdate']),
                'nonvisit': convert_to_bool_int(row['nonvisit']),
                'cancelled': convert_to_int(row['cancelled']),
            })
