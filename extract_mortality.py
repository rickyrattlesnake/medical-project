import csv
from load_pid_maps import load_pid_uuid_maps

pids, uuid_pid_map = load_pid_uuid_maps()

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pids)))


def convert_to_int(in_value):
    try:
        return int(float(str(in_value)))
    except ValueError:
        return ''


input_path = './csv/data_mortality_orig.csv'
output_path = './extracted_csv/pid_mortality.csv'

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
            'date_of_birth',
            'death_status',
            'date_of_death',
            'age_at_death',
            'location_at_death_code',
        ]
        writer = csv.DictWriter(out_file,
                                fieldnames=out_fieldnames,
                                extrasaction='raise')
        writer.writeheader()

        for row in filter(lambda row: len(row) > 0, reader):
            uuid = str(row['PATIENT_UID']).casefold()

            if uuid not in uuid_pid_map:
                raise ValueError('UUID not found in UUID_PID_MAP - {}'
                                 .format(uuid))

            writer.writerow({
                'pid_hash': uuid_pid_map[uuid],
                'date_of_birth': str(row['DOB']).strip().replace('/', '-'),
                'death_status': int(float(row['DECEASED_STATUS'])),
                'date_of_death': str(row['DEATH_DATE']).strip()
                                                       .replace('/', '-'),
                'age_at_death': convert_to_int(row['AGE_DEATH']),
                'location_at_death_code': convert_to_int(row['LOCATION_DEATH']),
            })
