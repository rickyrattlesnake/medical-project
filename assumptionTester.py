import csv
from savReaderWriter import SavReader


input_uuid_filename = './csv/ids_to_find.csv'
medSavFilename = './sav/all_past_medical_history_2016.sav'
diagSavFilename = './sav/all_diagnoses_2016.sav'

uuidColMed = 2
uuidColDiag = 2


all_ids = {}

with open(input_uuid_filename,
          mode='rt',
          errors='strict',
          encoding='utf-8') as uuidFile:
    reader = csv.reader(uuidFile,
                        delimiter=',',
                        quoting=csv.QUOTE_NONE,
                        strict=True)
    for row in reader:
        if len(row) >= 1:
            uuid = str(row[0]).casefold()
            all_ids[uuid] = {'med': 0, 'diag': 0}

med_ids = {}
with SavReader(medSavFilename) as medFile:
    for row in medFile:
        uuidMed = str(row[uuidColMed], 'utf-8').casefold()
        med_ids[uuidMed] = 0
        if uuidMed in all_ids:
            all_ids[uuidMed]['med'] = 1


patho_ids = {}
with SavReader(diagSavFilename) as diagFile:
    for row in diagFile:
        uuidDiag = str(row[uuidColDiag], 'utf-8').casefold()
        patho_ids[uuidDiag] = 0
        if uuidDiag in all_ids:
            all_ids[uuidDiag]['diag'] = 1

total_uuids = len(all_ids.keys())
print('Total uuids - {}'.format(total_uuids))

total_uuids_not_in_both = sum(1 if x['med'] == 0 and x['diag'] == 0 else 0
                              for x in all_ids.values())
print('Sum uuids not in both - {}'.format(total_uuids_not_in_both))

sum_only_in_med = sum(1 if x['med'] == 1 and x['diag'] == 0 else 0
                      for x in all_ids.values())
print('Sum only in med - {}'.format(sum_only_in_med))

sum_only_in_diag = sum(1 if x['diag'] == 1 and x['med'] == 0 else 0
                       for x in all_ids.values())
print('Sum only in diag - {}'.format(sum_only_in_diag))


sum_both_med_and_diag = sum(1 if x['diag'] == 1 and x['med'] == 1 else 0
                            for x in all_ids.values())
print('Sum only in both - {}'.format(sum_both_med_and_diag))





# print('Total Unique Patho Ids : {}'.format(len(patho_ids.keys())))
# print('Total Unique Demo Ids: {}'.format(len(med_ids.keys())))
# med_ids_found = sum(med_ids.values())
# print('DemoIds in Patho Ids: {}'.format(med_ids_found))
