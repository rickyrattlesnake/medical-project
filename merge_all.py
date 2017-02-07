import csv
from datetime import datetime
from load_pid_maps import load_pid_mapped_dataset, load_pid_uuid_maps
from utils import merge_boolean_fields, bool_to_int

# Create an empty data set from the pid map
pid_list, _ = load_pid_uuid_maps()
pid_merged_data = dict((pid, {}) for pid in pid_list)


def is_none_or_empty(in_value):
    val = str(in_value).strip()
    return val is None or val == ''


def parse_datetime(date_str):
    date_split = date_str.split('-')
    dt = datetime(year=int(date_split[0]),
                  month=int(date_split[1]),
                  day=int(date_split[2]))
    return dt


def check_safe_equality(left_val, right_val):
    left_val = str(left_val).strip().casefold()
    right_val = str(right_val).strip().casefold()
    return left_val == right_val


def transform_egfr_data(pid_list):
    in_file_path = './extracted_csv/pid_egfr.csv'
    out_path = './merged_csv/pid_egfr.csv'
    egfr_data = load_pid_mapped_dataset(in_file_path)

    pids_found = 0
    pids_not_found = 0
    pids_merged = 0
    pids_no_merge = 0

    merge_map = dict((pid, {}) for pid in pid_list)
    fields_to_merge = [
        'pid_hash',
        'egfr_measurement',
        'egfr_measurement_date'
    ]

    for pid in merge_map.keys():
        if pid not in egfr_data:
            pids_not_found += 1
            continue
        pids_found += 1
        merged_row = dict((f, None) for f in fields_to_merge)
        if len(egfr_data[pid]) == 1:
            pids_no_merge += 1
            merged_row.update(egfr_data[pid][0])
        else:
            merged_row.update(egfr_data[pid][0])
            merged_date = parse_datetime(merged_row['egfr_measurement_date'])
            for row in egfr_data[pid][1:]:
                pids_merged += 1
                row_date = parse_datetime(row['egfr_measurement_date'])
                if row_date > merged_date:
                    merged_row.update(row)
        merge_map[pid].update(merged_row)

    print('pids_found ' + str(pids_found))
    print('pids_not_found ' + str(pids_not_found))
    print('pids_merged ' + str(pids_merged))
    print('pids_no_merge ' + str(pids_no_merge))
    return (out_path, fields_to_merge, merge_map)


def transform_bmi_data(pid_list):
    in_file_path = './extracted_csv/pid_bmi.csv'
    out_path = './merged_csv/pid_bmi.csv'
    bmi_data = load_pid_mapped_dataset(in_file_path)

    pids_found = 0
    pids_not_found = 0
    pids_merged = 0
    pids_no_merge = 0

    merge_map = dict((pid, {}) for pid in pid_list)
    fields_to_merge = [
        'pid_hash',
        'bmi_measurement',
        'bmi_measurement_date'
    ]

    for pid in merge_map.keys():
        if pid not in bmi_data:
            pids_not_found += 1
            continue
        pids_found += 1
        merged_row = dict((f, None) for f in fields_to_merge)
        if len(bmi_data[pid]) == 1:
            pids_no_merge += 1
            merged_row.update(bmi_data[pid][0])
        else:
            merged_row.update(bmi_data[pid][0])
            merged_date = parse_datetime(merged_row['bmi_measurement_date'])
            for row in bmi_data[pid][1:]:
                pids_merged += 1
                row_date = parse_datetime(row['bmi_measurement_date'])
                if row_date > merged_date:
                    merged_row.update(row)
        merge_map[pid].update(merged_row)

    print('pids_found ' + str(pids_found))
    print('pids_not_found ' + str(pids_not_found))
    print('pids_merged ' + str(pids_merged))
    print('pids_no_merge ' + str(pids_no_merge))
    return (out_path, fields_to_merge, merge_map)


def transform_conditions_data(pid_list):
    in_file_path = './extracted_csv/pid_conditions.csv'
    out_path = './merged_csv/pid_conditions.csv'
    condition_data = load_pid_mapped_dataset(in_file_path)

    pids_found = 0
    pids_not_found = 0
    pids_merged = 0
    pids_no_merge = 0

    merge_map = dict((pid, {}) for pid in pid_list)
    fields_to_merge = [
        'pid_hash',
        'cancer',
        'metastatic_disease',
        'chemotherapy',
        'radiotherapy',
        'dementia',
        'chronic_heart_failure',
        'copd',
        'chronic_renal_failure',
        'stage_4_or_5_renal_failure',
        'dialysis',
        'chronic_liver_failure',
    ]

    for pid in merge_map.keys():
        if pid not in condition_data:
            pids_not_found += 1
            continue
        pids_found += 1
        merged_row = dict((f, None) for f in fields_to_merge)
        if len(condition_data[pid]) == 1:
            pids_no_merge += 1
            merged_row.update(condition_data[pid][0])
            for c in fields_to_merge[1:]:
                merged_row[c] = bool_to_int(condition_data[pid])
        else:
            merged_row.update(condition_data[pid][0])
            for c in fields_to_merge[1:]:
                dupe_values = [str(row[c]) for row in condition_data[pid]]
                merged_row[c] = merge_boolean_fields(dupe_values)
                pids_merged += 1
        merge_map[pid].update(merged_row)

    print('pids_found ' + str(pids_found))
    print('pids_not_found ' + str(pids_not_found))
    print('pids_merged ' + str(pids_merged))
    print('pids_no_merge ' + str(pids_no_merge))
    return (out_path, fields_to_merge, merge_map)


def write_csv(out_path, header_fields, csv_dict):
    with open(out_path, mode='wt', errors='strict',
              encoding='utf-8') as out_file:

        writer = csv.DictWriter(out_file,
                                fieldnames=header_fields,
                                extrasaction='raise')
        writer.writeheader()
        for pid, row in csv_dict.items():
            if len(row) != 0:
                if row.get('condition'):
                    del(row['condition'])
                if row.get('diagnosis_date'):
                    del(row['diagnosis_date'])
                writer.writerow(row)


def transform_mortality_data(merged_map):
    mortality_path = './extracted_csv/pid_mortality.csv'
    mortality_data = load_pid_mapped_dataset(mortality_path)
    fields_to_merge = [
        'pid_hash',
        'date_of_birth',
        'death_status',
        'date_of_death',
        'age_at_death',
        'location_at_death_code',
    ]

    pids_not_found = 0
    pids_merged = 0
    pids_no_merge = 0
    for pid in merged_map.keys():
        if pid not in mortality_data:
            pids_not_found += 1
            continue
        merged_row = dict((f, None) for f in fields_to_merge)
        if len(mortality_data[pid]) == 1:
            pids_no_merge += 1
            merged_row = mortality_data[pid][0]
        else:
            merged_row = mortality_data[pid][0]
            for row in mortality_data[pid][1:]:
                pids_merged += 1
                for f in fields_to_merge:
                    if not is_none_or_empty(row[f]):
                        merged_row[f] = row[f]
        merged_map[pid].update(merged_row)

    print('pids_not_found ' + str(pids_not_found))
    print('pids_merged ' + str(pids_merged))
    print('pids_no_merge ' + str(pids_no_merge))


out_path, out_headers, out_map = transform_conditions_data(pid_list)
write_csv(out_path, out_headers, out_map)

# out_path, out_headers, out_map = transform_egfr_data(pid_list)
# write_csv(out_path, out_headers, out_map)

# transform_mortality_data(pid_merged_data)

# output_path = './merged_csv/pid_merged_all.csv'
# with open(output_path, mode='wt', errors='strict',
#           encoding='utf-8') as out_file:
#     out_fieldnames = [
#         'pid_hash',
#         'date_of_birth',
#         'age_at_extraction',
#         'gender_code',
#         'atsi_code',
#         'site_id',
#         'death_status',
#         'date_of_death',
#         'age_at_death',
#         'location_at_death_code',
#         'bmi_measurement',
#         'bmi_measure_date',
#         'egfr_measurement',
#         'egfr_measurement_date',
#         'cancer',
#         'metastatic_disease',
#         'chemotherapy',
#         'radiotherapy',
#         'dementia',
#         'chronic_heart_failure',
#         'copd',
#         'chronic_renal_failure',
#         'stage_4_or_5_renal_failure',
#         'dialysis',
#         'chronic_liver_failure',
#     ]
#     writer = csv.DictWriter(out_file,
#                             fieldnames=out_fieldnames,
#                             extrasaction='raise')
#     writer.writeheader()

#     for pid, row in pid_merged_data.items():
#         writer.writerow(row)
