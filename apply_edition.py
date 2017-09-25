'''Module's Explanation Here
'''
import argparse
import csv
import re
import fileinput

def ApplyEdition(base_path, has_schema, edition_path):
    # First read the first changed line from edition_idx from diff.csv
    changed_line = 0
    edition_idx = int(re.search(r'\d+', edition_path).group())
    print "Edition_idx: ", edition_idx
    with open('data/diff.csv', 'rb') as diff_csv:
        reader = csv.reader(diff_csv)
        for row in reader:
            if int(row[0]) == edition_idx:
                changed_line = int(row[1])
    if has_schema:
        changed_line = changed_line + 1

    # Read edition csv line by line
    edition_csv = open(edition_path)
    ## Read the first line
    edition_line = edition_csv.readline()


    for idx, base_line in enumerate(fileinput.input(base_path, inplace=1)):
        if idx < changed_line:
            print base_line[:-1]
        elif edition_line:
            print edition_line[:-1]
            edition_line = edition_csv.readline()
        else:
            print base_line[:-1]

    edition_csv.close()
    print "Successful Edition"

def main():
    '''Script Entry Point
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('s', type=str, help="The path to base csv")
    parser.add_argument('b', type=str, help="The path to edition csv")
    parser.add_argument('--schema', dest='has_schema', action='store_true', help="Base csv contain the schema at first line. ")
    parser.add_argument('--no-schema', dest='has_schema', action='store_false', help="Base csv does not contain the schema at first line. ")
    parser.set_defaults(has_schema=False)
    args = parser.parse_args()

    ApplyEdition(args.s, args.has_schema, args.b)


if __name__ == '__main__':
    main()
