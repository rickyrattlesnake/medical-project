import csv
from savReaderWriter import SavReader
from datetime import datetime
from dataset_utils import load_mortality_metadata, UuidTracker


class Transformer:
    def __init__(self, in_path, out_path, tracker,
                 uuid_fieldname='patient_uuid'):
        self.in_path = in_path
        self.out_path = out_path
        self._filters = []
        self._tracker = tracker
        self._uuid_fieldname = uuid_fieldname

    def _all_filters_pass(self, dict_row):
        return all([fn(dict_row) for fn in self._filters])

    def addFilter(self, fieldnames=[], evaluator=lambda: False):
        def filterFn(dict_row):
            filter_args = [dict_row.get(f, None) for f in fieldnames]
            return evaluator(*filter_args)
        self._filters.append(filterFn)
        return self

    def transform(self):
        self._tracker.reset()
        with SavReader(self.in_path) as savData:
            with open(self.out_path, mode='wt', errors='strict',
                      encoding='utf8') as out_file:
                header = [str(field, 'utf8').casefold()
                          for field in savData.header]
                writer = csv.DictWriter(out_file,
                                        fieldnames=header,
                                        extrasaction='raise')
                writer.writeheader()

                for row in savData:
                    dict_row = {h: row[i].decode()
                                if type(row[i]) is bytes else row[i]
                                for (i, h) in enumerate(header)}
                    self._tracker.track_in_row()
                    if self._all_filters_pass(dict_row):
                        uuid = dict_row[self._uuid_fieldname]
                        self._tracker.track_uuid(uuid)
                        self._tracker.track_out_row()
                        writer.writerow(dict_row)
        self._tracker.print(self.out_path)


def uuid_filter_factory(uuid_collection):
    def uuid_filter(uuid):
        return str(uuid).casefold() in uuid_collection
    return uuid_filter


def record_date_filter_factory(max_record_date):
    def record_date_filter(record_date):
        record_date = str(record_date).split(' ')[0].split('-')
        record_date = datetime(year=int(record_date[0]),
                               month=int(record_date[1]),
                               day=int(record_date[2]))
        return record_date <= max_record_date
    return record_date_filter


def category_filter_factory(category_to_filter):
    def category_filter(category):
        return str(category).casefold() \
            == str(category_to_filter).casefold()
    return category_filter


def bool_filter_factory(bool_to_filter):
    def bool_filter(bool_str):
        bool_str = str(bool_str).strip().casefold()
        bool_val = None

        if bool_str in ['y', 'yes', 'true']:
            bool_val = True
        elif bool_str in ['n', 'no', 'false']:
            bool_val = False
        else:
            try:
                bool_val = bool(int(float(bool_str)))
            except ValueError:
                bool_val = None
        return bool_val == bool_to_filter or bool_val is None
    return bool_filter


def int_filter_factory(int_to_filter):
    def int_filter(num_str):
        num_str = str(num_str).strip()
        int_val = int(float(num_str)) if num_str else None
        return (int_val is None or int_to_filter == int_val)


if __name__ == '__main__':
    print('[-] Loading Mortality MetaData ...')
    mort_metadata = load_mortality_metadata(
        filepath='./csv/data_mortality_orig.csv',
        record_date_year_gap=1)
    max_record_date = mort_metadata['max_record_date']
    print('[*] Total UUIDs: {} | Total Dead UUIDs: {} | Max Record Date: {}'
          .format(len(mort_metadata['all_uuids']),
                  len(mort_metadata['dead_uuids']),
                  max_record_date))

    print('[-] Priming filters ...')
    uuid_filter = uuid_filter_factory(
        uuid_collection=mort_metadata['all_uuids'])
    record_date_filter = record_date_filter_factory(
        max_record_date=max_record_date)
    bmi_category_filter = category_filter_factory(
        category_to_filter='bmi')
    egfr_category_filter = category_filter_factory(
        category_to_filter='egfr')
    bool_true_filter = bool_filter_factory(True)
    bool_false_filter = bool_filter_factory(False)
    print('[v] Finished priming filters.')

    uuid_tracker = UuidTracker(all_uuids=mort_metadata['all_uuids'],
                               dead_uuids=mort_metadata['dead_uuids'])

    print('[-] Loading Transformers ...')
    demoTransformer = Transformer(
        in_path='./sav/all_demographic.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_demographic.csv') \
        .addFilter(['patient_uuid'], uuid_filter)
    diagTransformer = Transformer(
        in_path='./sav/all_diagnoses.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_diagnoses.csv') \
        .addFilter(['patient_uuid'], uuid_filter) \
        .addFilter(['diagnosis_date'], record_date_filter)
    measuresTransformer = Transformer(
        in_path='./sav/all_measures.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_bmi.csv') \
        .addFilter(['patient_uuid'], uuid_filter) \
        .addFilter(['measurement_datetime'], record_date_filter) \
        .addFilter(['type'], bmi_category_filter)
    medicalTransformer = Transformer(
        in_path='./sav/all_medical.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_medical.csv') \
        .addFilter(['patient_uuid'], uuid_filter) \
        .addFilter(['stamp_created_datetime'], record_date_filter)
    pathologyTransformer = Transformer(
        in_path='./sav/all_pathology.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_egfr.csv') \
        .addFilter(['patient_uuid'], uuid_filter) \
        .addFilter(['result_date'], record_date_filter) \
        .addFilter(['test_name'], egfr_category_filter)
    prescriptionsTransformer = Transformer(
        in_path='./sav/all_prescriptions.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_prescriptions.csv') \
        .addFilter(['patient_uuid'], uuid_filter)
    snapTransformer = Transformer(
        in_path='./sav/all_snap.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_snap.csv') \
        .addFilter(['patient_uuid'], uuid_filter)
    visitsTransformer = Transformer(
        in_path='./sav/all_visits.sav',
        tracker=uuid_tracker,
        out_path='./filtered_csv/filtered_visits.csv') \
        .addFilter(['patient_uuid'], uuid_filter) \
        .addFilter(['nonvisit'], bool_false_filter) \
        .addFilter(['cancelled'], bool_false_filter)

    transformer_collection = [
        demoTransformer,
        diagTransformer,
        measuresTransformer,
        medicalTransformer,
        pathologyTransformer,
        # prescriptionsTransformer,
        # snapTransformer,
        # visitsTransformer,
    ]

    print('[-] Starting to filter datasets.')

    for t in transformer_collection:
        t.transform()

    print('[v] Finished filtering datasets.')
