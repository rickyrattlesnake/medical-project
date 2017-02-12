# medical-project

----------------ASSUMPTIONS -----------------
Assumptions made with Dataset Extraction & Transformation:

[-] EGFR measurements had string values to denote above / below a certain level.
    These were converted to boundary value.
    E.g. '<^10' => 9.0. '> 90' and '>^90' converted to 91.0

[-] Gender Codes:
    Female = 1, Male = 0, Unknown = 2

[-] Location at death was a code but not sure what they mean.

[-] nonvisit was a boolean string. This was converted to a int representation
    E.g. 'y' => 1, 'n' => 0, '' => ''


-------------- TO DO ---------------------------------
v Remove 'test' rows
v Mapping between patient(first, last, dob) => patient_hash
v Mapping between UUID => patient_hash
v Merge to single file with extracted data - unique PIDs

- New data set 2 years relative


--------------PROGRAM OUTPUT ------------------------
++++++++++++++++++++++ Generate PIDs ++++++++++++++++++++++++++
Creating Unique PID to UUIDs map from ./csv/data_mortality_orig.csv ...
Writing PID to UUID map file to ./csv/uuid_pid_map.csv ...
Uuid Statistics ---
Total unique_pid = 24903
PID Occurence Counter { #occurences : #pids } = Counter({1: 24014, 2: 857, 3: 30, 4: 1, 5: 1})
###################### One Year Window (Max Record Date 2015-11-12) Filtering ####################
++++++++++++++++++++++ Filtering +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
[-] Loading Filter UUIDs from ./csv/data_mortality_orig.csv ...
[-] Total UUIDs to find = 25827
[-] Total Dead UUIDs to find = 1166
[-] Maximum Death Date = 2016-11-12 00:00:00
[-] Maximum Record Date = 2015-11-12 00:00:00
[-] Filtering prescriptions :: ./sav/all_prescriptions.sav to ./filtered_csv/filtered_prescriptions.csv ...
['patient_uuid', 'reason', 'trade_name', 'therclass', 'script_date']
[v] Total rows in data file = 2333363
[v] UUIDs founds = 20871
[v] Dead UUIDs found = 948
[-] Filtering diagnoses :: ./sav/all_diagnoses.sav to ./filtered_csv/filtered_diagnoses.csv ...
['patient_uuid', 'diagnosis_date', 'reason']
[v] Total rows in data file = 1250587
[v] UUIDs founds = 15036
[v] Dead UUIDs found = 764
[-] Filtering visits :: ./sav/all_visits.sav to ./filtered_csv/filtered_visits.csv ...
['patient_uuid', 'visitdate', 'nonvisit', 'cancelled']
[v] Total rows in data file = 2001860
[v] UUIDs founds = 17950
[v] Dead UUIDs found = 624
[-] Filtering measures :: ./sav/all_measures.sav to ./filtered_csv/filtered_bmi.csv ...
['patient_uuid', 'type', 'measurement', 'measurement_datetime']
[v] Total rows in data file = 3462347
[v] UUIDs founds = 3056
[v] Dead UUIDs found = 112
[-] Filtering medical :: ./sav/all_medical.sav to ./filtered_csv/filtered_medical.csv ...
['patient_uuid', 'condition', 'stamp_created_datetime', 'stamp_datetime', 'active', 'year_transpired', 'month_transpired']
[v] Total rows in data file = 453839
[v] UUIDs founds = 15910
[v] Dead UUIDs found = 823
[-] Filtering demographic :: ./sav/all_demographic.sav to ./filtered_csv/filtered_demographic.csv ...
['patient_uuid', 'gender_code', 'dob', 'atsi', 'ageatextraction', 'site_id']
[v] Total rows in data file = 170892
[v] UUIDs founds = 25827
[v] Dead UUIDs found = 1166
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
++++++++++++++++++++++++++++++++++++++ Extraction ++++++++++++++++++++++++++++++++++++++++++
[-] Collecting PID and UUID maps from ./csv/uuid_pid_map.csv
++++++++++++++++++++++++++++++++++++++ Merge +++++++++++++++++++++++++++++++++++++++++++++++
// no output
// no output
################################# Two Year Window Max Date (2014/11/12) #############################
[-] Loading Filter UUIDs from ./csv/data_mortality_orig.csv ...
[-] Total UUIDs to find = 25827
[-] Total Dead UUIDs to find = 1166
[-] Maximum Death Date = 2016-11-12 00:00:00
[-] Maximum Record Date = 2014-11-12 00:00:00
[-] Filtering medical :: ./sav/all_medical.sav to ./filtered_csv/filtered_medical.csv ...
['patient_uuid', 'condition', 'stamp_created_datetime', 'stamp_datetime', 'active', 'year_transpired', 'month_transpired']
[v] Total rows in data file = 453839
[v] UUIDs founds = 15064
[v] Dead UUIDs found = 811
[-] Filtering pathology :: ./sav/all_pathology.sav to ./filtered_csv/filtered_egfr.csv ...
['patient_uuid', 'result_date', 'test_name', 'result', 'units', 'normal_range']
[v] Total rows in data file = 5244191
[v] UUIDs founds = 4310
[v] Dead UUIDs found = 191
[-] Filtering prescriptions :: ./sav/all_prescriptions.sav to ./filtered_csv/filtered_prescriptions.csv ...
['patient_uuid', 'reason', 'trade_name', 'therclass', 'script_date']
[v] Total rows in data file = 2333363
[v] UUIDs founds = 20871
[v] Dead UUIDs found = 948
[-] Filtering diagnoses :: ./sav/all_diagnoses.sav to ./filtered_csv/filtered_diagnoses.csv ...
['patient_uuid', 'diagnosis_date', 'reason']
[v] Total rows in data file = 1250587
[v] UUIDs founds = 14357
[v] Dead UUIDs found = 756
[-] Filtering snap :: ./sav/all_snap.sav to ./filtered_csv/filtered_snap.csv ...
['patient_uuid', 'smoker', 'smokes_per_day', 'alcohol_consumption']
[v] Total rows in data file = 170172
[v] UUIDs founds = 25825
[v] Dead UUIDs found = 1166
[-] Filtering measures :: ./sav/all_measures.sav to ./filtered_csv/filtered_bmi.csv ...
['patient_uuid', 'type', 'measurement', 'measurement_datetime']
[v] Total rows in data file = 3462347
[v] UUIDs founds = 2738
[v] Dead UUIDs found = 112
[-] Filtering visits :: ./sav/all_visits.sav to ./filtered_csv/filtered_visits.csv ...
['patient_uuid', 'visitdate', 'nonvisit', 'cancelled']
[v] Total rows in data file = 2001860
[v] UUIDs founds = 17950
[v] Dead UUIDs found = 624
[-] Filtering demographic :: ./sav/all_demographic.sav to ./filtered_csv/filtered_demographic.csv ...
['patient_uuid', 'gender_code', 'dob', 'atsi', 'ageatextraction', 'site_id']
[v] Total rows in data file = 170892
[v] UUIDs founds = 25827
[v] Dead UUIDs found = 1166
[-] Collecting PID and UUID maps from ./csv/uuid_pid_map.csv
################################### 3 Year Windows (Max Date 2013/11/12) #########################
[-] Loading Filter UUIDs from ./csv/data_mortality_orig.csv ...
[-] Total UUIDs to find = 25827
[-] Total Dead UUIDs to find = 1166
[-] Maximum Death Date = 2016-11-12 00:00:00
[-] Maximum Record Date = 2013-11-12 00:00:00
[-] Filtering visits :: ./sav/all_visits.sav to ./filtered_csv/filtered_visits.csv ...
['patient_uuid', 'visitdate', 'nonvisit', 'cancelled']
[v] Total rows in data file = 2001860
[v] UUIDs founds = 17950
[v] Dead UUIDs found = 624
[-] Filtering demographic :: ./sav/all_demographic.sav to ./filtered_csv/filtered_demographic.csv ...
['patient_uuid', 'gender_code', 'dob', 'atsi', 'ageatextraction', 'site_id']
[v] Total rows in data file = 170892
[v] UUIDs founds = 25827
[v] Dead UUIDs found = 1166
[-] Filtering diagnoses :: ./sav/all_diagnoses.sav to ./filtered_csv/filtered_diagnoses.csv ...
['patient_uuid', 'diagnosis_date', 'reason']
[v] Total rows in data file = 1250587
[v] UUIDs founds = 13698
[v] Dead UUIDs found = 749
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
[-] Filtering pathology :: ./sav/all_pathology.sav to ./filtered_csv/filtered_egfr.csv ...
['patient_uuid', 'result_date', 'test_name', 'result', 'units', 'normal_range']
[v] Total rows in data file = 5244191
[v] UUIDs founds = 3696
[v] Dead UUIDs found = 181
[-] Filtering measures :: ./sav/all_measures.sav to ./filtered_csv/filtered_bmi.csv ...
['patient_uuid', 'type', 'measurement', 'measurement_datetime']
[v] Total rows in data file = 3462347
[v] UUIDs founds = 2429
[v] Dead UUIDs found = 103
[-] Filtering medical :: ./sav/all_medical.sav to ./filtered_csv/filtered_medical.csv ...
['patient_uuid', 'condition', 'stamp_created_datetime', 'stamp_datetime', 'active', 'year_transpired', 'month_transpired']
[v] Total rows in data file = 453839
[v] UUIDs founds = 14233
[v] Dead UUIDs found = 799
[-] Collecting PID and UUID maps from ./csv/uuid_pid_map.csv
