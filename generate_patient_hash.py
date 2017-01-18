import csv
import hashlib
import collections

input_uuid_col = 0
last_name_col = 1
first_name_col = 2
dob_col = 3

input_uuid_file = './csv/data_mortality_orig.csv'
output_uuid_pid_file = './csv/uuid_to_unique_pid_map.csv'
# PatientID key is defined as (lastname, firstname, dob)
# as a concantenated string
# PatientID Hash is a non-reversible hash of the PatientID key

# There maybe multiple uuids that map to same PID

print('Creating Unique PID to UUIDs map from {} ...'
      .format(input_uuid_file))
pid_to_uuids_map = {}
with open(input_uuid_file,
          mode='rt',
          errors='strict',
          encoding='utf-8') as uuid_data:
    reader = csv.reader(uuid_data,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    headerRow = next(reader)

    for row in reader:
        last_name = row[last_name_col].strip()
        first_name = row[first_name_col].strip()
        dob = row[dob_col].strip()

        pid = ''.join([last_name, first_name, dob]).casefold()
        uuid = str(row[input_uuid_col]).strip().casefold()

        if not pid or not uuid:
            raise ValueError('PID or UUID is empty : row - {}'
                             .format(row))

        if pid in pid_to_uuids_map:
            pid_to_uuids_map[pid].append(uuid)
        else:
            pid_to_uuids_map[pid] = [uuid]

print('Writing PID to UUID map file to {} ...'
      .format(output_uuid_pid_file))
with open(output_uuid_pid_file,
          mode='wt',
          errors='strict',
          encoding='utf-8') as outputFile:
    writer = csv.writer(outputFile,
                        delimiter=',',
                        quoting=csv.QUOTE_MINIMAL,
                        strict=True)
    writer.writerow(['graphite_uuid', 'hashed_pid', 'pid'])

    for (pid, uuids) in pid_to_uuids_map.items():
        hash_algo = hashlib.sha256()
        hash_algo.update(bytes(pid, 'utf-8'))
        hashed_pid = hash_algo.hexdigest()
        rows = [(uuid, hashed_pid, pid) for uuid in uuids]
        writer.writerows(rows)

print('Uuid Statistics ---')
print('Total unique_pid = {}'.format(len(pid_to_uuids_map)))
print('PID Occurence Counter {{ #occurences : #pids }} = {}'
      .format(collections.Counter(len(x)
                                  for x in pid_to_uuids_map.values()
                                  )))
