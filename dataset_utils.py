import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta


def load_mortality_metadata(filepath,
                            record_date_year_gap=1,
                            uuid_fieldname='PATIENT_UID',
                            death_status_fieldname='DECEASED_STATUS',
                            death_date_fieldname='DEATH_DATE'):

    uuid_death_dates = load_uuid_death_dates(filepath)
    max_death_date = max(uuid_death_dates.values(),
                         key=lambda d: datetime(1, 1, 1)
                         if d is None else d)
    all_uuids = set(uuid_death_dates.keys())
    dead_uuids = set(uuid for uuid, date in uuid_death_dates.items()
                     if date is not None)

    max_record_date = max_death_date - \
        relativedelta(years=record_date_year_gap)

    return {
        'all_uuids': all_uuids,
        'dead_uuids': dead_uuids,
        'max_death_date': max_death_date,
        'max_record_date': max_record_date,
    }


def load_uuid_death_dates(filepath,
                          uuid_fieldname='PATIENT_UID',
                          death_status_fieldname='DECEASED_STATUS',
                          death_date_fieldname='DEATH_DATE'):
    uuid_death_dates = {}
    with open(filepath,
              mode='rt',
              errors='strict',
              encoding='utf-8') as mortalityFile:
        reader = csv.DictReader(mortalityFile, strict=True)

        for row in reader:
            uuid = str(row[uuid_fieldname]).casefold()
            death_date = None
            if row[death_status_fieldname] == '1':
                death_date = row[death_date_fieldname].split('/')
                death_date = datetime(year=int(death_date[2]),
                                      month=int(death_date[1]),
                                      day=int(death_date[0]))
            uuid_death_dates[uuid] = death_date
    return uuid_death_dates


class UuidTracker():
    def __init__(self, all_uuids, dead_uuids):
        self._all_uuids_tracker = {str(uuid).casefold(): False
                                   for uuid in all_uuids}
        self._dead_uuids_tracker = {str(uuid).casefold(): False
                                    for uuid in dead_uuids}
        self._out_row_count = 0
        self._in_row_count = 0

    def reset(self):
        for key in self._all_uuids_tracker.keys():
            self._all_uuids_tracker[key] = False
        for key in self._dead_uuids_tracker.keys():
            self._dead_uuids_tracker[key] = False
        self._out_row_count = 0
        self._in_row_count = 0

    def track_out_row(self):
        self._out_row_count += 1

    def track_in_row(self):
        self._in_row_count += 1

    def track_uuid(self, uuid):
        uuid = str(uuid).casefold()
        if uuid in self._all_uuids_tracker:
            self._all_uuids_tracker[uuid] = True
        if uuid in self._dead_uuids_tracker:
            self._dead_uuids_tracker[uuid] = True

    def print(self, preamble=''):
        dead_found = sum(int(v) for v in self._dead_uuids_tracker.values())
        all_found = sum(int(v) for v in self._all_uuids_tracker.values())
        print('[*] ' + preamble)
        print('[*] Input row count = {}'.format(self._in_row_count))
        print('[*] Output row count = {}'.format(self._out_row_count))
        print('[*] All UUIDs found = {}'.format(all_found))
        print('[*] Dead UUIDs found = {}'.format(dead_found))
        print()
