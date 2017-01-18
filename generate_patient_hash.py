import csv
import hashlib

input_file = './csv/patient_data_ids.csv'
dupe_maps_file = './csv/dupe-merge/all.csv'

# pid_to_uuid_file = './csv/pid_uuid_map.csv'
uuid_to_hashed_pid_file = './csv/uuid_to_pid_map.csv'

dupe_map = {}
with open(dupe_maps_file,
          mode='rt',
          errors='strict',
          encoding='utf-8') as dupe_file:
    reader = csv.reader(dupe_file,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    headerRow = next(reader)
    # for (col, val) in enumerate(headerRow):
    #     print('col : {} - val : {}'.format(col, val))

    for row in reader:
        concat_pid_input = ''.join(str(x, 'utf-8').strip()
                                   if type(x) is bytes else x
                                   for x in row[1:4]).casefold()
        uuids = [x.strip().casefold() for x in row[0].split(':')]
        if concat_pid_input == '':
            raise ValueError('no pid or uuids - row - {}'.format(row))
        dupe_map[concat_pid_input] = uuids

pid_to_uuids_map = {}
with open(input_file,
          mode='rt',
          errors='strict',
          encoding='utf-8') as orig_data:
    reader = csv.reader(orig_data,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    headerRow = next(reader)

    for row in reader:
        concat_pid = ''.join(str(x, 'utf-8').strip().casefold()
                             if type(x) is bytes else x
                             for x in row[0:3]).casefold()
        uuid = str(row[9]).casefold()
        if concat_pid == '' or len(uuids) == 0:
            raise ValueError('no pid or uuids - row - {}'.format(row))
        if concat_pid in dupe_map:
            pid_to_uuids_map[concat_pid] = dupe_map[concat_pid]
        else:
            pid_to_uuids_map[concat_pid] = [uuid]


with open(uuid_to_hashed_pid_file,
          mode='wt',
          errors='strict',
          encoding='utf-8') as orig_data:
    writer = csv.writer(orig_data,
                        delimiter=',',
                        quoting=csv.QUOTE_MINIMAL,
                        strict=True)
    writer.writerow(['graphite_uuid', 'hashed_pid', 'pid'])

    for (pid, uuids) in pid_to_uuids_map.items():
        hash_algo = hashlib.sha256()
        hash_algo.update(bytes(pid, 'utf-8'))
        hashed_pid = hash_algo.hexdigest()
        rows = [(uuid, hashed_pid, pid)
                for uuid in uuids]
        writer.writerows(rows)

print('Finished :: Stats')
print('Total unique_pid = {}'.format(len(pid_to_uuids_map.keys())))

duped_counter = {}
for uuids in pid_to_uuids_map.values():
    if len(uuids) in duped_counter:
        duped_counter[len(uuids)] += 1
    else:
        duped_counter[len(uuids)] = 1
print('Uniquified Uuids Counts : {}'.format(duped_counter))
