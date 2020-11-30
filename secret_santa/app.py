#!/usr/bin/env python3
import argparse  # do I need to say more?
import csv  # pretty much only used to check the file
import random  # for the matching
import sys  # dem error codes

# My modules
from mail import bootstrap  # my email function


def check_csv(fileh):
    dialect = csv.Sniffer().sniff(fileh.read())
    if dialect().delimiter != ',':
        print("INVALID")
        sys.exit(22)
    else:
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-m", "--email")
    parser.add_argument("-s", "--smtp")
    # parser.add_argument("", kwargs)
    args = parser.parse_args()
    try:
        with open(args.input, 'r') as csvfile:
            # check_csv(csvfile)
            lines = csvfile.readlines()
            people = {}
            i = 0
            for row in lines:
                people[i-1] = row.split(",")
                i += 1
            csvfile.close()  # close my file like a good boy
    except IOError:
        print("not valid file path")
        sys.exit(2)

    del people[-1]  # delete the label row
    # it works because its a dictionary =
    # removing the trailing newlines that are made when spliting
    for i in people:
        people.get(i)[-1] = people.get(i)[-1].replace("\n", "")
    # start of the matching
    people_copy = people.copy()
    matches = {}
    i = 0
    x = 0
    while bool(people_copy) is not False:
        x = random.choice(list(people_copy.keys()))
        if x == i:
            continue
        matches[i] = x
        del people_copy[x]
        i += 1
    bootstrap(people, matches, args.email, args.smtp)
    sys.exit()
