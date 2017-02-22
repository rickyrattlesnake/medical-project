import csv
from dataset_utils import load_mortality_metadata
from diagnosis_classification import classify


mort_path = './csv/data_mortality_orig.csv'
mort_meta = load_mortality_metadata(filepath=mort_path)
diag_path = './filtered_csv/filtered_diagnoses.csv'
med_path = './filtered_csv/filtered_medical.csv'


def run_program(file_path, fieldname, class_to_test):
    print('Running for {}'.format(file_path))
    with open(file_path) as in_file:
        reader = csv.DictReader(in_file)

        found_uuids = set()
        for row in reader:
            uuid = str(row['patient_uuid']).casefold()
            diag_str = row[fieldname]
            diag_class = classify(diag_str)
            if(diag_class[class_to_test] == 1):
                found_uuids.add(uuid)
        print('Found {} UUIDS'.format(len(found_uuids)))

        mort_meta = load_mortality_metadata(filepath=mort_path)
        print('Dead UUIDS {}'
              .format(sum(1 for uuid in found_uuids
                          if uuid in mort_meta['dead_uuids'])))
        print('Alive UUIDS {}'
              .format(sum(1 for uuid in found_uuids
                          if uuid not in mort_meta['dead_uuids'])))


run_program(diag_path, 'reason', 'cancer')
run_program(med_path, 'condition', 'cancer')
