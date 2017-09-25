'''Genenate the workload to compare orpheusDB and UStore

'''

import argparse
import csv
import random as rand

fieldnames = ['ID', 'Name', 'Age', 'Profile']

def RandomStr(length):
    '''Create the random string of given length
    '''
    letters = "abcdefghijklmnokqrsuvwyzABCDEFGHIJKLMSOPQRSUVWXYZ"
    return ''.join(rand.choice(letters) for i in range(length))


def RandomInt(lower, upper):
    '''Return a random int from [lower, upper) that sample randomly
    '''
    return rand.randint(lower, upper)


def DumpCSV(dest_path, dest_sm_path, num_records):
    ''' Generate workload and dump to csv file.

    Each record consists of the following four fields:
      * ID: an Increasing counter of type int
      * Name: a string within 10 chars
      * Age: a int between [0, 100]
      * Descrption: a string of length between [50, 150]

    Roughly, each record takes up 100B. Records are sorted in
    increasing order by Age.

    Args:
      dest_path: string The path to the destination csv without schema
      dest_sm_path: string The path to the destination csv with schema
      num_record: int  The number of records to generate
    '''


    csvfile = open(dest_path, 'wb')
    sm_csvfile = open(dest_sm_path, 'wb')

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    sm_writer = csv.DictWriter(sm_csvfile, fieldnames=fieldnames)
    sm_writer.writeheader()
    for i in range(num_records):
        ID = i + 1
        name = RandomStr(RandomInt(5, 10))
        age = ID * 100  / num_records # Age are in increasing order.
        profile =  RandomStr(RandomInt(50, 150))

        writer.writerow({"ID": ID,
                         "Name": name,
                         "Age": age,
                         "Profile": profile})

        sm_writer.writerow({"ID": ID,
                            "Name": name,
                            "Age": age,
                            "Profile": profile})

    csvfile.close()
    sm_csvfile.close()

def EditCSV(src_path, dest_path, num_records, num_changed, edited_age):
    '''Edit the src file with num_changed records based on age.
       Dump the edition to dest_path. src file is kept unchanged.

    Args:
      src_path: string. The path to src csv file with schema
      dest_path: string. The path to csv file that contains the new edition.
      num_records: Number of records in src file
      num_changed: Number of records to edit
      edited_age: int. The records within edited_age will be edited.
                       E.g, if it is 10, the profile of the preceding
                       num_changed record with age between [10, 19] will be edited.

      The src file will be kept unchanged. Only the edition part will be dumped
      to dest_path

    Return the line of first changed tuples.
    '''
    src_csv = open(src_path)
    dest_csv = open(dest_path, 'wb')

    reader = csv.DictReader(src_csv)
    writer = csv.DictWriter(dest_csv, fieldnames=fieldnames)

    line = 0
    edited_count = 0
    edition = False
    changed_line = 0

    for record in reader:
        age = int(record["Age"])
        if not edition and age / 10 == edited_age / 10:
            edition = True
            changed_line = line # Record down the line of first edition

        if edition and edited_count < num_changed:
            ID = record["ID"]
            name = record["Name"]
            profile =  RandomStr(RandomInt(50, 150))
            writer.writerow({"ID": ID,
                             "Name": name,
                             "Age": age,
                             "Profile": profile})

            edited_count = edited_count + 1

        if age / 10 > edited_age / 10:
            edition = False

        line = line + 1

    dest_csv.close()
    src_csv.close()
    return changed_line

def WriteSchema(schema_path):
    '''Write the schema to given path
    '''
    with open(schema_path, 'wb') as schema_csv:
        writer = csv.writer(schema_csv)
        writer.writerow(['ID', 'text'])
        writer.writerow(['Name', 'text'])
        writer.writerow(['Age', 'text'])
        writer.writerow(['Profile', 'text'])



def GenerateWorkload(num_records, num_edition):
    '''Generate the workload

    * Each workload is different from previous worload by ratio
    percentage of records. Different records are grouped continuously.
    * diff.csv logs the changed tuple index and length

    Args:
      num_workloads: int
      num_records: int Number of records in each workload
    '''
    base_csv = "data/base.csv"
    base_sm_csv = "data/base_sm.csv"
    WriteSchema("data/schema.csv")
    DumpCSV(base_csv, base_sm_csv, num_records)

    edition_csvs = ["data/edition_" + str(i) + ".csv" for i in range(10)]

    changed_idxs = []
    for i, edition_csv in enumerate(edition_csvs):
        changed_idx = EditCSV(base_sm_csv, edition_csv,  num_records, num_edition, 10 * i)
        changed_idxs.append(changed_idx)

    with open("data/diff.csv", 'wb') as diff_csv:
        writer = csv.writer(diff_csv)
        for idx in range(10):
            writer.writerow([idx, changed_idxs[idx]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('r', type=int, help="Number of records in the workload")
    parser.add_argument('e', type=int, help="Number of edited records")
    args = parser.parse_args()

    GenerateWorkload(args.r, args.e)


if __name__ == '__main__':
    main()
