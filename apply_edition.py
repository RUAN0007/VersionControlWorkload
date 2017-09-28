'''Module's Explanation Here
'''
import argparse
import csv
import re
import fileinput
import random as rand

def RandomStr(length):
    '''Create the random string of given length
    '''
    letters = "abcdefghijklmnokqrsuvwyzABCDEFGHIJKLMSOPQRSUVWXYZ"
    return ''.join(rand.choice(letters) for i in range(length))

def ApplyEdition(base_path, has_schema, selected_age, selected_region):
    edited_count = 0
    for i, base_line in enumerate(fileinput.input(base_path, inplace=1)):
        if has_schema and i == 0:
            print base_line[:-1]
            continue
        fields = base_line.split(',')

        if selected_age == fields[2] and selected_region == fields[3]:
            edited_count = edited_count + 1
            ID = fields[0]
            name = fields[1]
            age = fields[2]
            region = fields[3]
            num_departure = fields[4]
            profile = RandomStr(rand.randint(50, 150))
            print ",".join([ID, name, age, region, num_departure, profile])
        else:
            print base_line[:-1]
    return edited_count


def main():
    '''Script Entry Point
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('b', type=str, help="The path to base csv")
    parser.add_argument('a', type=str, help="A two-digit string for records of age to edit")
    parser.add_argument('r', type=str, help="Records of region to edit")
    parser.add_argument('--schema', dest='has_schema', action='store_true', help="Base csv contain the schema at first line. ")
    parser.add_argument('--no-schema', dest='has_schema', action='store_false', help="Base csv does not contain the schema at first line. ")
    parser.set_defaults(has_schema=False)
    args = parser.parse_args()

    print ApplyEdition(args.b, args.has_schema, args.a, args.r)


if __name__ == '__main__':
    main()
