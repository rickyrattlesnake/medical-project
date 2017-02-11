import csv


class Merger():
    def __init__(self,
                 in_paths,
                 out_path,
                 pid_field_map='pid_hash'):
        self.in_paths = in_paths
        self.out_path = out_path
        self._fieldnames = self.infer_header()
        self._pid_field_name = pid_field_map

    def infer_header(self):
        with open(self.in_paths[0],
                  mode='rt',
                  errors='strict',
                  encoding='utf-8') as in_file:
            headers = csv.DictReader(in_file, strict=True).fieldnames
            headers = [h for h in headers
                       if h not in self.get_ignored_fields()]
            return headers

    def get_ignored_fields(self):
        return []

    def get_pid(self, row):
        return str(row[self._pid_field_name]).casefold()

    def merge_row(self, existing_row, new_row):
        raise NotImplementedError('Implement in SubClass.')

    def _bool_str_or(self, val1, val2):
        return int(int(val1) or int(val2))

    def _create_merged_map(self):
        merged_pid_rows = {}

        for filepath in self.in_paths:
            with open(filepath,
                      mode='rt',
                      errors='strict',
                      encoding='utf-8') as in_file:
                reader = csv.DictReader(in_file, strict=True)
                for row in reader:
                    pid = self.get_pid(row)
                    if pid in merged_pid_rows:
                        merged_pid_rows[pid] = \
                            self.merge_row(merged_pid_rows[pid], row)
                    else:
                        merged_pid_rows[pid] = self.merge_row(row, row)

        return merged_pid_rows

    def merge(self):
        merged_map = self._create_merged_map()
        with open(self.out_path,
                  mode='wt',
                  errors='strict',
                  encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file,
                                    fieldnames=self._fieldnames,
                                    extrasaction='raise')
            writer.writeheader()
            for pid, merged_row in merged_map.items():
                writer.writerow(merged_row)


class ConditionsMerger(Merger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_ignored_fields(self):
        return ['condition', 'diagnosis_date']

    def merge_row(self, existing_row, new_row):
        merged_row = {}
        merge_fn = {
            'pid_hash': lambda old, new: new,
            'cancer': self._bool_str_or,
            'metastatic_disease': self._bool_str_or,
            'chemotherapy': self._bool_str_or,
            'radiotherapy': self._bool_str_or,
            'dementia': self._bool_str_or,
            'chronic_heart_failure': self._bool_str_or,
            'copd': self._bool_str_or,
            'chronic_renal_failure': self._bool_str_or,
            'stage_4_or_5_renal_failure': self._bool_str_or,
            'dialysis': self._bool_str_or,
            'chronic_liver_failure': self._bool_str_or,
        }

        for field_name in self._fieldnames:
            if field_name not in merge_fn:
                raise ValueError('Field Name not found in merge_fn.')
            merged_row[field_name] = \
                merge_fn[field_name](existing_row[field_name],
                                     new_row[field_name])
        return merged_row


conditions_merger = ConditionsMerger(
    in_paths=[
        './extracted_csv/pid_medical.csv',
        './extracted_csv/pid_diagnoses.csv'
    ],
    out_path='./merged_csv/merged_conditions.csv')
conditions_merger.merge()
