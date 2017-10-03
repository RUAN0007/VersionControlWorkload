# Workload Generation
```
python generate_workload <num_records> <num_age> <num_region>
```

NOTE: the max of <num_region> is 20. The max of <num_age> is 90.

This above command will generate 3 files in data/. 

base.csv and base_sm.csv(with schema at first line) will contain <num_records> records, sorted by age and then by region.

Each record will consist of six fields and takes 100B:
* ID: monotonically increasing from 0 to <num_records> - 1. Fixed at 12 digit. 
* Name: A random string of length between (5, 10) chars.
* Age: int between [5, 5 + <num_age>] in two digit format uniformly
* Region: one of specified region 
* Num_Departure: an int following zipt distribution in two digit format
* Profile: a random string of length between (50, 150) chars. 

schema.csv will contain the schema required by orpheusDB. 

# Apply edition
```
python apply_edition [--no-schema | schema] <path_to_edited_base> <age> <region>
```
The above command will edit the profile of records of specified age and region. 
