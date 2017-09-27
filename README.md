# Workload Generation
```
python generate_workload <num_records> <num_region>
```

NOTE: the max of num_region is 20. 

This above command will generate 3 files in data/. 

base.csv and base_sm.csv(with schema at first line) will contain <num_records> records, sorted by age and then by region.

Each record will consist of four fields and takes 100B:
* ID: monotonically increasing from 0 to num_records - 1
* Name: A random string of length between (5, 10) chars.
* Age: int bewtween [5, 95] in two digit format uniformly
* Region: one of specified region 
* Num_Departure: an int following zipt distribution in two digit format
* Profile: a random string of length between (50, 150) chars. 

schema.csv will contain the schema required by orpheusDB. 

# Apply edition
```
python apply_edition [--no-schema | schema] <path_to_edited_base> <age> <region>
```
The above command will edit the profile of records of specified age and region. 
