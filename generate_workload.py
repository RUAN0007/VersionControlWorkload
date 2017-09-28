'''Genenate the workload to compare orpheusDB and UStore

'''
import os
import argparse
import csv
import random as rand
import numpy as np

fieldnames = ['ID', 'Name', 'Age', 'Region', 'Num_Departure', 'Profile']

sg_regions = ['Bedok', 'Jurong_West', 'Tampines', 'Woodlands', 'Hougang',
              'Sengkang', 'Yishun', 'Ang_Mo_Kio', 'Choa_Chu_Kang', 'Bukit_Merah',
              'Pasir_Ris', 'Bukit_Batok', 'Bukit_Panjang', 'Toa_Payoh', 'Serangoon',
              'Geylang', 'Punggol', 'Kallang', 'Queenstown', 'Clementi']

def RandomStr(length):
    '''Create the random string of given length
    '''
    letters = "abcdefghijklmnokqrsuvwyzABCDEFGHIJKLMSOPQRSUVWXYZ"
    return ''.join(rand.choice(letters) for i in range(length))


def ZipfInt(a):
    '''Return a random int following zipf distribution

    The return type is a two-digit string
    '''
    r = np.random.zipf(a)
    while r > 100:
        r = np.random.zipf(a)
    return '%02d' % r

def DumpCSV(dest_path, dest_sm_path, num_records, num_regions):
    ''' Generate workload and dump to csv file.

    Each record consists of the following four fields:
      * ID: an Increasing counter of type int
      * Name: a string within 10 chars
      * Age: a uniform two-digit int between [5, 95]
      * Region: THe resident region in sg
      * Num_Depeature: a two-digit int following zipf distribution
      * Profile: a string of length between [50, 150]

    Roughly, each record takes up 100B. Records are sorted in
    increasing order by Age. Region as the secondary key

    Args:
      dest_path: string The path to the destination csv without schema
      dest_sm_path: string The path to the destination csv with schema
      num_record: int  The number of records to generate
      num_region: int The number of distinct regions among all records
    '''


    csvfile = open(dest_path, 'wb')
    sm_csvfile = open(dest_sm_path, 'wb')

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    sm_writer = csv.DictWriter(sm_csvfile, fieldnames=fieldnames)
    sm_writer.writeheader()
    for i in range(num_records):
        ID = "%012d" % (i + 1)
        name = RandomStr(rand.randint(5, 10))
        num_same_age = num_records / 90 + 1
        age = '%02d' % (i / num_same_age + 5) # Age are in increasing order.
        num_same_region = num_records / 90 / num_regions + 1
        region = sg_regions[i % num_same_age / num_same_region]
        num_departure = ZipfInt(2)
        profile =  RandomStr(rand.randint(50, 150))

        writer.writerow({"ID": ID,
                         "Name": name,
                         "Age": age,
                         "Region": region,
                         "Num_Departure": num_departure,
                         "Profile": profile})

        sm_writer.writerow({"ID": ID,
                            "Name": name,
                            "Age": age,
                            "Region": region,
                            "Num_Departure": num_departure,
                            "Profile": profile})

    print "Dump csv with schema to " + dest_sm_path
    print "Dump csv without schema to " + dest_path
    csvfile.close()
    sm_csvfile.close()


def WriteSchema(schema_path):
    '''Write the schema to given path
    '''
    with open(schema_path, 'wb') as schema_csv:
        writer = csv.writer(schema_csv)
        for field in fieldnames:
            writer.writerow([field, 'text'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('r', type=int, help="Number of records in the workload")
    parser.add_argument('e', type=int, help="Number of Distinctive Regions")
    args = parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_csv = dir_path + "/data/base.csv"
    base_sm_csv = dir_path + "/data/base_sm.csv"
    WriteSchema(dir_path + "/data/schema.csv")
    DumpCSV(base_csv, base_sm_csv, args.r, args.e)


if __name__ == '__main__':
    main()
