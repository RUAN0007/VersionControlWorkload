# Workload Generation
```
python generate_workload <num_records> <num_edition>
```

This above command will generate 14 files in data/. 

base.csv and base_sm.csv(with schema at first line) will contain <num_records> records, sorted by age.

Each record will consist of four fields and takes 100B:
* ID: monotonically increasing from 0 to num_records - 1
* Name: A random string of length between (5, 10) chars.
* Age: int bewtween [0, 99]
* Profile: a random string of length between (50, 150) chars. 

schema.csv will contain the schema required by orpheusDB. 

For edition_x.csv (x can be ranged from 0 to 9), each contains the edited records from base.csv that the Profile of first <num_edition> records between age (10x and 10x + 10) will be changed. 

diff.csv records down the first edited line in base.csv for edition_x.csv

# Apply edition
```
python apply_edition [--no-schema | schema] <path_to_edited_base> <path_to_edition>
```

The above command will apply the edition in <path_to_edition> to <path_to_edited_base>. The option --no-schema implies that the <path_to_edited_base> csv does not contain schema at first line. The option --schema is the opposite. 
