#!/usr/bin/env python3
import argparse
import sys
import csv
import random


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
    # parser.add_argument("", kwargs)
    args = parser.parse_args()
    try:
        with open(args.input, 'r') as csvfile:
            # check_csv(csvfile)
            lines = csvfile.readlines()
            people = {}
            i = 0
            for row in lines:
                people[i] = row.split(",")
                i += 1

            del people[0]  # delete the lable row

            people_copy = people
            matches = {}
            i = 0
            while people_copy is not False:
                x = random.choice(list(people_copy.keys()))
                print(x, i)
                # print(len(list(people_copy.keys())))
                if i == x:
                    continue
                    print("con")
                else:
                    matches[i] = x
                    del people_copy[x]
                    print(i)
                i += 1
            print(matches)
            sys.exit()
    except IOError:
        print("not valid file path")
        sys.exit(2)
