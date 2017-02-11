import csv
from diagnosis_classification import classify


def extract(cache):
    paths = [
        './extracted_csv/pid_diagnoses.csv',
        './extracted_csv/pid_medical.csv',
    ]

    for path in paths:
        with open(path,
                  mode='rt',
                  errors='strict',
                  encoding='utf-8') as in_file:
            reader = csv.DictReader(in_file, strict=True)

            for row in reader:
                cond = row['condition']
                cache_condition(cond,
                                classify(cond),
                                cache)


def cache_condition(condition, classification, cache):
    for c, is_in in classification.items():
        if is_in:
            cache[c]['in'].add(condition)
        else:
            cache[c]['out'].add(condition)


def write_out(cache):
    out_file_path = './assumptions/{}_{}.txt'
    for c, in_out in cache.items():
        for k, cond_list in in_out.items():
            with open(out_file_path.format(c, k),
                      mode='wt',
                      errors='strict',
                      encoding='utf-8') as out_file:
                out_file.writelines([str(x) + '\n'
                                     for x in cond_list])


classes = [
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

classification_cache = {c: {'in': set(), 'out': set()}
                        for c in classes}
extract(classification_cache)
write_out(classification_cache)
