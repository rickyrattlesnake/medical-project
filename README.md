# medical-project

ASSUMPTIONS -----------------
Assumptions made with Dataset Extraction & Transformation:

[-] EGFR measurements had string values to denote above / below a certain level.
    These were converted to boundary value.
    E.g. '<^10' => 9.0. '> 90' and '>^90' converted to 91.0

[-] Gender Codes:
    Female = 1, Male = 0, Unknown = 2

[-] Location at death was a code but not sure what they mean.

[-] nonvisit was a boolean string. This was converted to a int representation
    E.g. 'y' => 1, 'n' => 0, '' => ''


TO DO ------------
v Remove 'test' rows
v Mapping between patient(first, last, dob) => patient_hash
v Mapping between UUID => patient_hash
- Merge to single file with extracted data - unique PIDs

- New data set 2 years relative

- Mortality Info (



