# medical-project

To Do >>
v Remove 'test' rows
v Mapping between patient(first, last, dob) => patient_hash
v Mapping between UUID => patient_hash

- Mapping of (finalFile, field) to (File, column name)
- Merge ? (delimit with |)
- Merge ? (highlight weird merges)
- End up with one giant raw data file

? are there dupes for people that died - no



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


