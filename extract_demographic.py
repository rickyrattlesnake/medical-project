import csv
from load_pid_maps import load_pid_uuid_maps

pids, uuid_pid_map = load_pid_uuid_maps()

print('[v] Total UUIDS - {}'.format(len(uuid_pid_map)))
print('[v] Total PIDs - {}'.format(len(pids)))


def generate_gender_code(gender_in):
    gender = str(gender_in).strip().casefold()
    if gender == 'm':
        return 0
    elif gender == 'f':
        return 1
    else:
        return 2


input_path = './filtered_csv/filtered_demographic.csv'
output_path = './extracted_csv/pid_demographic.csv'

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
            'gender_code',
            'date_of_birth',
            'age_at_extraction',
            'atsi_code',
            'site_id',
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
                'gender_code': generate_gender_code(row['gender_code']),
                'date_of_birth': str(row['dob']).split(' ')[0],
                'age_at_extraction': int(float(row['ageatextraction'])),
                'atsi_code': int(float(row['atsi'])),
                'site_id': int(float(row['site_id'])),
            })
