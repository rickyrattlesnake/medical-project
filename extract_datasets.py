import csv
import re
from load_pid_maps import load_pid_uuid_maps


class Extractor():
    def __init__(self,
                 in_path,
                 out_path,
                 out_fields,
                 uuid_pid_map,
                 id_field_name='patient_uuid'):
        self.in_path = in_path
        self.out_path = out_path
        self._uuid_pid_map = uuid_pid_map
        self._out_fields = out_fields
        self._id_field_name = id_field_name

    def get_uuid(self, row):
        return str(row[self._id_field_name]).casefold()

    def get_pid(self, row):
        uuid = self.get_uuid(row)
        return str(self._uuid_pid_map[uuid]).casefold()

    def extract_fields(self, row):
        """args:
                row - csvDict row to transform and extract.
           returns:
                dict - a mapping of {'out_field_name' => 'extracted_value'}
        """
        raise NotImplementedError('Must be implemented in SubClass!')

    def strip_date(self, date_time_str):
        return str(date_time_str).split(' ')[0]

    def strip_float(self, float_str):
        return str(float_str)

    def strip_floor_int(self, number_str):
        return int(float(str(number_str)))

    def extract(self):
        # Open the input file
        with open(self.in_path,
                  mode='rt',
                  errors='strict',
                  encoding='utf-8') as in_file:
            reader = csv.DictReader(in_file, strict=True)
            with open(self.out_path,
                      mode='wt',
                      errors='strict',
                      encoding='utf-8') as out_file:
                writer = csv.DictWriter(out_file,
                                        fieldnames=self._out_fields,
                                        extrasaction='raise')
                writer.writeheader()

                for row in filter(lambda row: len(row) > 0, reader):
                    uuid = self.get_uuid(row)

                    # Extract and transform specific fields
                    extracted_fields = self.extract_fields(row)

                    if uuid not in self._uuid_pid_map:
                        raise ValueError('UUID not found in UUID_PID_MAP - {}'
                                         .format(uuid))
                    writer.writerow(extracted_fields)


class BmiExtractor(Extractor):
    def __init__(self, in_path, out_path, uuid_pid_map):
        out_fields = [
            'pid_hash',
            'bmi_measurement',
            'bmi_measurement_date',
        ]
        super().__init__(in_path=in_path,
                         out_path=out_path,
                         uuid_pid_map=uuid_pid_map,
                         out_fields=out_fields)

    def extract_fields(self, row):
        measurement_date = self.strip_date(row['measurement_datetime'])
        return {
            'pid_hash': self.get_pid(row),
            'bmi_measurement': self.strip_float(row['measurement']),
            'bmi_measurement_date': measurement_date,
        }


class DemographicExtractor(Extractor):
    def __init__(self, *args, **kwargs):
        out_fields = [
            'pid_hash',
            'gender_code',
            'date_of_birth',
            'age_at_extraction',
            'atsi_code',
            'site_id',
        ]
        super().__init__(out_fields=out_fields,
                         *args,
                         **kwargs)

    def parse_gender_code(self, gender):
        gender_str = str(gender).strip().casefold()
        if gender_str == 'm':
            return 0
        elif gender_str == 'f':
            return 1
        else:
            return 2

    def extract_fields(self, row):
        return {
            'pid_hash': self.get_pid(row),
            'gender_code': self.parse_gender_code(row['gender_code']),
            'date_of_birth': self.strip_date(row['dob']),
            'age_at_extraction': self.strip_floor_int(row['ageatextraction']),
            'atsi_code': self.strip_floor_int(row['atsi']),
            'site_id': self.strip_floor_int(row['site_id']),
        }


class EgfrExtractor(Extractor):
    def __init__(self, *args, **kwargs):
        out_fields = [
            'pid_hash',
            'egfr_measurement',
            'egfr_measurement_date',
        ]
        super().__init__(out_fields=out_fields, *args, **kwargs)

    def parse_egfr_score(self, in_value):
        score = str(in_value).strip()
        if re.match(r'>.?90', score):
            return 91.0
        elif re.match(r'<.?10', score):
            return 9.0
        else:
            return float(score)

    def extract_fields(self, row):
        return {
            'pid_hash': self.get_pid(row),
            'egfr_measurement': self.parse_egfr_score(row['result']),
            'egfr_measurement_date': self.strip_date(row['result_date']),
        }


if __name__ == '__main__':
    pids, uuid_pid_map = load_pid_uuid_maps()
    extractor_pool = []
    extractor_pool.extend([
        BmiExtractor(in_path='./filtered_csv/filtered_bmi.csv',
                     out_path='./extracted_csv/pid_bmi_2.csv',
                     uuid_pid_map=uuid_pid_map),
        DemographicExtractor(in_path='./filtered_csv/filtered_demographic.csv',
                             out_path='./extracted_csv/pid_demographic_2.csv',
                             uuid_pid_map=uuid_pid_map),
        EgfrExtractor(in_path='./filtered_csv/filtered_egfr.csv',
                      out_path='./extracted_csv/pid_egfr_2.csv',
                      uuid_pid_map=uuid_pid_map)
    ])
    list(map(lambda ex: ex.extract(), extractor_pool))
