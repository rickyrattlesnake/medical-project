import csv
from dataset_utils import load_mortality_metadata
# from load_pid_maps import load_pid_uuid_maps

# find pids with conditions
final_merge_path = './datasets_max_2015/merged_all.csv'
diag_path = './datasets_max_2015/pid_diagnoses.csv'
med_path = './datasets_max_2015/pid_medical.csv'
cond_path = './datasets_max_2015/merged_conditions.csv'
uuid_pid_path = './csv/uuid_pid_map.csv'
mort_path = './csv/data_mortality_orig.csv'


def load_pid_to_uuid_maps():
    pid_uuids = {}
    with open(uuid_pid_path, mode='rt') as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:
            pid = row['hashed_pid']
            uuid = row['graphite_uuid']
            if pid in pid_uuids:
                pid_uuids[pid].append(uuid)
            else:
                pid_uuids[pid] = [uuid]
    return pid_uuids


def run_program(file_path):
    print('Running for {}'.format(file_path))
    with open(file_path) as in_file:
        reader = csv.DictReader(in_file)

        found_pids = set()
        for row in reader:
            if(row['chemotherapy'] == '1'):
                found_pids.add(row['pid_hash'])
        print('Found {} PIDs'.format(len(found_pids)))

        found_uuids = set()
        pid_uuids = load_pid_to_uuid_maps()
        for pid in found_pids:
            for uuid in pid_uuids[pid]:
                found_uuids.add(uuid)
        print('Found {} UUIDs'.format(len(found_uuids)))
        mort_meta = load_mortality_metadata(filepath=mort_path)
        print('Dead UUIDS {}'
              .format(sum(1 for uuid in found_uuids
                          if uuid in mort_meta['dead_uuids'])))
        print('Alive UUIDS {}'
              .format(sum(1 for uuid in found_uuids
                          if uuid not in mort_meta['dead_uuids'])))


run_program(diag_path)
run_program(med_path)
run_program(cond_path)
