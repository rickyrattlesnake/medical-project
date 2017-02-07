# medical-project

CODES:

gender_code : Female = 1, Male = 0, Unknown = 2
location_at_death_code: ???

NOTES:::
[?] egfr scores <^10 => converted to 9.0, > 90 >^90 converted to 91.0
[?] nonvisit => y / n  to 1 / 0 (empty string if blank)


To Do >>
v Remove 'test' rows
v Mapping between patient(first, last, dob) => patient_hash
v Mapping between UUID => patient_hash
- Mapping of (finalFile, field) to (File, column name)
V Merge ? (delimit with "||")
V Merge ? (highlight weird merges)
- End up with one giant raw data file
v - are there dupes for people that died - no
v - 

[v] all_measaure.sav -> all_bmi.sav
[v] all_pathology -> all_gfri
[v] merged to patient_id_conditions

[-] extract all filtered data sets into pid_*.csv datasets
[-] merge into singular pids for each pid_*.csv
[-] merge into a single file for analysis

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

========================= Filtering ==============
[-] Loading Filter UUIDs from ./csv/data_mortality_orig.csv ...
[-] Total UUIDs to find = 25827
[-] Total Dead UUIDs to find = 1166
[-] Maximum Death Date = 2016-11-12 00:00:00
[-] Maximum Record Date = 2015-11-12 00:00:00
[-] Filtering diagnoses :: ./sav/all_diagnoses.sav to ./filtered_csv/filtered_diagnoses.csv ...
['patient_uuid', 'diagnosis_date', 'reason']
[v] Total rows in data file = 1250587
[v] UUIDs founds = 15036
[v] Dead UUIDs found = 764
[-] Filtering demographic :: ./sav/all_demographic.sav to ./filtered_csv/filtered_demographic.csv ...
['patient_uuid', 'gender_code', 'dob', 'atsi', 'ageatextraction', 'site_id']
[v] Total rows in data file = 170892
[v] UUIDs founds = 25827
[v] Dead UUIDs found = 1166
[-] Filtering medical :: ./sav/all_medical.sav to ./filtered_csv/filtered_medical.csv ...
['patient_uuid', 'condition', 'stamp_created_datetime', 'stamp_datetime', 'active', 'year_transpired', 'month_transpired']
[v] Total rows in data file = 453839
[v] UUIDs founds = 15910
[v] Dead UUIDs found = 823
[-] Filtering measures :: ./sav/all_measures.sav to ./filtered_csv/filtered_bmi.csv ...
['patient_uuid', 'type', 'measurement', 'measurement_datetime']
[v] Total rows in data file = 3462347
[v] UUIDs founds = 3056
[v] Dead UUIDs found = 112
[-] Filtering pathology :: ./sav/all_pathology.sav to ./filtered_csv/filtered_egfr.csv ...
['patient_uuid', 'result_date', 'test_name', 'result', 'units', 'normal_range']
[v] Total rows in data file = 5244191
[v] UUIDs founds = 4748
[v] Dead UUIDs found = 199
[-] Filtering snap :: ./sav/all_snap.sav to ./filtered_csv/filtered_snap.csv ...
['patient_uuid', 'smoker', 'smokes_per_day', 'alcohol_consumption']
[v] Total rows in data file = 170172
[v] UUIDs founds = 25825
[v] Dead UUIDs found = 1166
[-] Filtering prescriptions :: ./sav/all_prescriptions.sav to ./filtered_csv/filtered_prescriptions.csv ...
['patient_uuid', 'reason', 'trade_name', 'therclass', 'script_date']
[v] Total rows in data file = 2333363
[v] UUIDs founds = 20871
[v] Dead UUIDs found = 948
[-] Filtering visits :: ./sav/all_visits.sav to ./filtered_csv/filtered_visits.csv ...
['patient_uuid', 'visitdate', 'nonvisit', 'cancelled']
[v] Total rows in data file = 2001860
[v] UUIDs founds = 17950
[v] Dead UUIDs found = 624


=========================

----- Merging ./csv/filtered_demographic.csv to ./merged_csv/merged_demographic.csv ...
Total rows in data file = 25827
Total unique UUIDs = 25827
----- End Merging Results -----
----- Merging ./csv/filtered_snap.csv to ./merged_csv/merged_snap.csv ...
Total rows in data file = 25825
Total unique UUIDs = 25825
----- End Merging Results -----
----- Merging ./csv/filtered_measures.csv to ./merged_csv/merged_measures.csv ...
Total rows in data file = 584252
Total unique UUIDs = 13334
----- End Merging Results -----
----- Merging ./csv/filtered_medical.csv to ./merged_csv/merged_medical.csv ...
Total rows in data file = 108605
Total unique UUIDs = 16301
----- End Merging Results -----
----- Merging ./csv/filtered_diagnoses.csv to ./merged_csv/merged_diagnoses.csv ...
Total rows in data file = 156844
Total unique UUIDs = 15412
----- End Merging Results -----
----- Merging ./csv/filtered_pathology.csv to ./merged_csv/merged_pathology.csv ...
Total rows in data file = 1166245
Total unique UUIDs = 6696
----- End Merging Results -----
----- Merging ./csv/filtered_prescriptions.csv to ./merged_csv/merged_prescriptions.csv ...
Total rows in data file = 618208
Total unique UUIDs = 20871
----- End Merging Results -----
----- Merging ./csv/filtered_visits.csv to ./merged_csv/merged_visits.csv ...
Total rows in data file = 416647
Total unique UUIDs = 17950
----- End Merging Results -----
