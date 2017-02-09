import csv


def load_pid_uuid_maps():
    uuid_pid_path = './csv/uuid_pid_map.csv'
    uuid_pid_map = {}
    pids = set()

    print('[-] Collecting PID and UUID maps from {}'
          .format(uuid_pid_path))

    with open(uuid_pid_path,
              mode='rt',
              errors='strict',
              encoding='utf-8') as uuid_pid_file:
        reader = csv.reader(uuid_pid_file, strict=True)
        # ignore header row
        next(reader)

        for row in filter(lambda row: len(row) > 0, reader):
            uuid = str(row[0]).casefold()
            pid_hash = str(row[1]).casefold()

            if not pid_hash or not uuid:
                raise ValueError('PID or UUID is empty : row - {}'
                                 .format(row))

            uuid_pid_map[uuid] = pid_hash
            pids.add(pid_hash)

    return (pids, uuid_pid_map)


def load_pid_mapped_dataset(filepath, pid_col_name='pid_hash'):
    pid_mapped_dataset = {}

    with open(filepath, mode='rt', errors='strict',
              encoding='utf-8') as source_file:
        reader = csv.DictReader(source_file, strict=True)

        for row in filter(lambda row: len(row) > 0, reader):
            pid_hash = str(row[pid_col_name]).casefold()

            if pid_hash in pid_mapped_dataset:
                pid_mapped_dataset[pid_hash].append(row)
            else:
                pid_mapped_dataset[pid_hash] = [row]
    return pid_mapped_dataset
