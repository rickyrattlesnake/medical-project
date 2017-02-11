import csv


class DatasourceMerger():
    def __init__(self,
                 in_paths,
                 out_path,
                 pid_field_name='pid_hash'):
        self.in_paths = in_paths
        self.out_path = out_path
        self._merged_headers = list(self.collate_headers())
        self._merge_cache = {}
        self._pid_field_name = pid_field_name

    def collate_headers(self):
        all_headers = []
        for path in self.in_paths:
            with open(path,
                      mode='rt',
                      errors='strict',
                      encoding='utf-8') as in_file:
                reader = csv.DictReader(in_file, strict=True)
                all_headers.extend(f for f in reader.fieldnames
                                   if f not in all_headers)
        return all_headers

    def get_pid(self, row):
        return str(row[self._pid_field_name]).casefold()

    def merge_row(self, row):
        pid = self.get_pid(row)
        if pid not in self._merge_cache:
            self._merge_cache[pid] = {
                field: '' for field in self._merged_headers
            }
        self._merge_cache[pid].update(row)

    def merge_all(self):
        for filepath in self.in_paths:
            with open(filepath,
                      mode='rt',
                      errors='strict',
                      encoding='utf-8') as in_file:
                reader = csv.DictReader(in_file, strict=True)
                for row in reader:
                    self.merge_row(row)

        with open(self.out_path,
                  mode='wt',
                  errors='strict',
                  encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file,
                                    fieldnames=self._merged_headers,
                                    extrasaction='raise')
            writer.writeheader()
            for merged_row in self._merge_cache.values():
                writer.writerow(merged_row)


ds_merger = DatasourceMerger(
    in_paths=[
        './extracted_csv/pid_bmi.csv',
        './extracted_csv/pid_demographic.csv',
        './extracted_csv/pid_egfr.csv',
        './extracted_csv/pid_mortality.csv',
        './merged_csv/merged_conditions.csv',
    ],
    out_path='./merged_csv/merged_all.csv')

ds_merger.merge_all()
