import csv
import re
from load_pid_maps import load_pid_uuid_maps
from diagnosis_classification import classify as classify_diagnosis
from dataset_utils import load_mortality_metadata, load_uuid_death_dates


class Extractor():
    def __init__(self,
                 in_path,
                 out_path,
                 out_fields,
                 uuid_pid_map,
                 uuid_field_name='patient_uuid'):
        self.in_path = in_path
        self.out_path = out_path
        self._uuid_pid_map = uuid_pid_map
        self._out_fields = out_fields
        self._uuid_field_name = uuid_field_name

    def get_uuid(self, row):
        return str(row[self._uuid_field_name]).casefold()

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

    def strip_str(self, in_val):
        return str(in_val).strip()

    def strip_date(self, date_time_str):
        return (str(date_time_str).split(' ')[0]
                if date_time_str else '')

    def strip_float(self, float_str):
        return str(float_str)

    def strip_floor_int(self, num_val):
        num_str = str(num_val)
        return int(float(str(num_str))) if num_str else ''

    def strip_bool_int(self, in_bool_str):
        bool_str = str(in_bool_str).strip().casefold()
        if bool_str in ['y', 'yes', 'true', '1']:
            return 1
        elif bool_str in ['n', 'no', 'false', '0']:
            return 0
        else:
            return ''

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
                    if extracted_fields is not None:
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


class VisitsExtractor(Extractor):
    def __init__(self,
                 dead_uuids,
                 uuid_death_dates,
                 filter_dead,
                 *args,
                 **kwargs):
        self._dead_uuids = dead_uuids
        self._filter_dead = filter_dead
        self._uuid_death_dates = uuid_death_dates
        out_fields = [
            'pid_hash',
            'visit_date',
            'is_dead',
            'death_date',
        ]
        super().__init__(out_fields=out_fields,
                         *args,
                         **kwargs)

    def _is_dead(self, row):
        return self.get_uuid(row) in self._dead_uuids

    def _get_death_date(self, row):
        return self._uuid_death_dates[self.get_uuid(row)]

    def extract_fields(self, row):
        is_dead = self._is_dead(row)
        if self._filter_dead != is_dead:
            return None

        result = {
            'pid_hash': self.get_pid(row),
            'visit_date': self.strip_date(row['visitdate']),
        }
        if is_dead:
            result['death_date'] = self.strip_date(self._get_death_date(row))
        return result


class SnapExtractor(Extractor):
    def __init__(self, *args, **kwargs):
        out_fields = [
            'pid_hash',
            'smoker',
            'smokes_per_day',
            'alcohol_consumption',
        ]
        super().__init__(out_fields=out_fields,
                         *args,
                         **kwargs)

    def extract_fields(self, row):
        alcohol_cons = self.strip_floor_int(row['alcohol_consumption'])
        return {
            'pid_hash': self.get_pid(row),
            'smoker': self.strip_str(row['smoker']),
            'smokes_per_day': self.strip_floor_int(row['smokes_per_day']),
            'alcohol_consumption': alcohol_cons,
        }


class MortalityExtractor(Extractor):
    def __init__(self, *args, **kwargs):
        out_fields = [
            'pid_hash',
            'date_of_birth',
            'death_status',
            'date_of_death',
            'age_at_death',
            'location_at_death_code',
        ]
        super().__init__(out_fields=out_fields,
                         uuid_field_name='PATIENT_UID',
                         *args,
                         **kwargs)

    def normalise_date(self, date_str):
        return date_str.strip().replace('/', '-')

    def extract_fields(self, row):
        return {
            'pid_hash': self.get_pid(row),
            'date_of_birth': self.normalise_date(row['DOB']),
            'death_status': self.strip_bool_int(row['DECEASED_STATUS']),
            'date_of_death': self.normalise_date(row['DEATH_DATE']),
            'age_at_death': self.strip_floor_int(row['AGE_DEATH']),
            'location_at_death_code':
                self.strip_floor_int(row['LOCATION_DEATH']),
        }


class PrescriptionExtractor(Extractor):
    def __init__(self, dead_uuids, uuid_death_dates, *args, **kwargs):
        self._dead_uuids = dead_uuids
        self._uuid_death_dates = uuid_death_dates
        out_fields = [
            'pid_hash',
            'ther_class',
            'script_date',
            'is_opioid',
            'is_dead',
            'death_date',
        ]
        super().__init__(out_fields=out_fields,
                         *args,
                         **kwargs)

    def _is_dead(self, row):
        return int(self.get_uuid(row) in self._dead_uuids)

    def _get_death_date(self, row):
        return self._uuid_death_dates[self.get_uuid(row)]

    def _is_opioid(self, drug_class):
        return int(str(drug_class).strip().casefold() in
                   ['na', 'nac', 'nan'])

    def extract_fields(self, row):
        return {
            'pid_hash': self.get_pid(row),
            'ther_class': self.strip_str(row['therclass']),
            'script_date': self.strip_date(row['script_date']),
            'is_opioid': self._is_opioid(row['therclass']),
            'is_dead': self._is_dead(row),
            'death_date': self.strip_date(self._get_death_date(row))
        }


class MedicalExtractor(Extractor):
    def __init__(self, *args, **kwargs):
        out_fields = [
            'pid_hash',
            'condition',
            'diagnosis_date',
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
        super().__init__(out_fields=out_fields,
                         *args,
                         **kwargs)

    def extract_fields(self, row):
        field_map = classify_diagnosis(row['condition'])
        field_map.update({
            'pid_hash': self.get_pid(row),
            'condition': self.strip_str(row['condition']),
            'diagnosis_date': self.strip_date(row['stamp_created_datetime'])
        })
        return field_map


class DiagnosesExtractor(Extractor):
    def __init__(self, *args, **kwargs):
        out_fields = [
            'pid_hash',
            'condition',
            'diagnosis_date',
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
        super().__init__(out_fields=out_fields,
                         *args,
                         **kwargs)

    def extract_fields(self, row):
        field_map = classify_diagnosis(row['reason'])
        field_map.update({
            'pid_hash': self.get_pid(row),
            'condition': self.strip_str(row['reason']),
            'diagnosis_date': self.strip_date(row['diagnosis_date'])
        })
        return field_map


if __name__ == '__main__':
    pids, uuid_pid_map = load_pid_uuid_maps()
    mort_metadata = load_mortality_metadata(
        filepath='./csv/data_mortality_orig.csv'
    )
    uuid_death_dates = load_uuid_death_dates(
        filepath='./csv/data_mortality_orig.csv'
    )

    extractor_pool = [
        # BmiExtractor(
        #     in_path='./filtered_csv/filtered_bmi.csv',
        #     out_path='./extracted_csv/pid_bmi.csv',
        #     uuid_pid_map=uuid_pid_map),
        # DemographicExtractor(
        #     in_path='./filtered_csv/filtered_demographic.csv',
        #     out_path='./extracted_csv/pid_demographic.csv',
        #     uuid_pid_map=uuid_pid_map),
        # EgfrExtractor(
        #     in_path='./filtered_csv/filtered_egfr.csv',
        #     out_path='./extracted_csv/pid_egfr.csv',
        #     uuid_pid_map=uuid_pid_map),
        VisitsExtractor(
            in_path='./filtered_csv/filtered_visits.csv',
            out_path='./extracted_csv/pid_live_visits.csv',
            dead_uuids=mort_metadata['dead_uuids'],
            uuid_death_dates=uuid_death_dates,
            uuid_pid_map=uuid_pid_map,
            filter_dead=False),
        VisitsExtractor(
            in_path='./filtered_csv/filtered_visits.csv',
            out_path='./extracted_csv/pid_dead_visits.csv',
            dead_uuids=mort_metadata['dead_uuids'],
            uuid_death_dates=uuid_death_dates,
            uuid_pid_map=uuid_pid_map,
            filter_dead=True),

        # SnapExtractor(
        #     in_path='./filtered_csv/filtered_snap.csv',
        #     out_path='./extracted_csv/pid_snap.csv',
        #     uuid_pid_map=uuid_pid_map),
        # MortalityExtractor(
        #     in_path='./csv/data_mortality_orig.csv',
        #     out_path='./extracted_csv/pid_mortality.csv',
        #     uuid_pid_map=uuid_pid_map),
        # PrescriptionExtractor(
        #     in_path='./filtered_csv/filtered_prescriptions.csv',
        #     out_path='./extracted_csv/pid_prescriptions.csv',
        #     dead_uuids=mort_metadata['dead_uuids'],
        #     uuid_death_dates=uuid_death_dates,
        #     uuid_pid_map=uuid_pid_map),x
        # MedicalExtractor(
        #     in_path='./filtered_csv/filtered_medical.csv',
        #     out_path='./extracted_csv/pid_medical.csv',
        #     uuid_pid_map=uuid_pid_map),
        # DiagnosesExtractor(
        #     in_path='./filtered_csv/filtered_diagnoses.csv',
        #     out_path='./extracted_csv/pid_diagnoses.csv',
        #     uuid_pid_map=uuid_pid_map),
    ]
    list(map(lambda ex: ex.extract(), extractor_pool))
