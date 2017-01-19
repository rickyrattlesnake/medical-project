# medical-project

To Do >>
v Remove 'test' rows
v Mapping between patient(first, last, dob) => patient_hash
v Mapping between UUID => patient_hash
- Mapping of (finalFile, field) to (File, column name)
V Merge ? (delimit with ";")
V Merge ? (highlight weird merges)
- End up with one giant raw data file
v - are there dupes for people that died - no
v - 


-----------------------
what i did -

removed 2 rows of testing data = new total matched rows = 25827
- testing rows were not in duped data file

---Running Generate_patient_hash
Creating Unique PID to UUIDs map from ./csv/data_mortality_orig.csv ...
Writing PID to UUID map file to ./csv/uuid_to_unique_pid_map.csv ...
Uuid Statistics ---
Total unique_pid = 24903
PID Occurence Counter { #occurences : #pids } = Counter({1: 24014, 2: 857, 3: 30, 4: 1, 5: 1})

----------------------------
Loading Filter UUIDs from ./csv/data_mortality_orig.csv ...
Filtering ./sav/all_pathology.sav to ./csv/filtered_pathology.csv ...
['patient_uuid', 'result_date', 'test_name', 'result', 'units', 'normal_range']
Filtering statistics --- 
Total rows in data file = 5244191
Total UUIDs to find = 25827
UUIDs founds = 6696
Filtering ./sav/all_diagnoses.sav to ./csv/filtered_diagnoses.csv ...
['patient_uuid', 'diagnosis_date', 'reason']
Filtering statistics --- 
Total rows in data file = 1250587
Total UUIDs to find = 25827
UUIDs founds = 15412
Filtering ./sav/all_visits.sav to ./csv/filtered_visits.csv ...
['patient_uuid', 'visitdate', 'nonvisit', 'cancelled']
Filtering statistics --- 
Total rows in data file = 2001860
Total UUIDs to find = 25827
UUIDs founds = 17950
Filtering ./sav/all_measures.sav to ./csv/filtered_measures.csv ...
['patient_uuid', 'type', 'measurement', 'measurement_datetime']
Filtering statistics --- 
Total rows in data file = 3462347
Total UUIDs to find = 25827
UUIDs founds = 13334
Filtering ./sav/all_prescriptions.sav to ./csv/filtered_prescriptions.csv ...
['patient_uuid', 'reason', 'trade_name', 'therclass', 'script_date']
Filtering statistics --- 
Total rows in data file = 2333363
Total UUIDs to find = 25827
UUIDs founds = 20871
Filtering ./sav/all_medical.sav to ./csv/filtered_medical.csv ...
['patient_uuid', 'condition', 'stamp_created_datetime', 'stamp_datetime', 'active', 'year_transpired', 'month_transpired']
Filtering statistics --- 
Total rows in data file = 453839
Total UUIDs to find = 25827
UUIDs founds = 16301
Filtering ./sav/all_snap.sav to ./csv/filtered_snap.csv ...
['patient_uuid', 'smoker', 'smokes_per_day', 'alcohol_consumption']
Filtering statistics --- 
Total rows in data file = 170172
Total UUIDs to find = 25827
UUIDs founds = 25825
Filtering ./sav/all_demographic.sav to ./csv/filtered_demographic.csv ...
['patient_uuid', 'gender_code', 'dob', 'atsi', 'ageatextraction', 'site_id']
Filtering statistics --- 
Total rows in data file = 170892
Total UUIDs to find = 25827
UUIDs founds = 25827
