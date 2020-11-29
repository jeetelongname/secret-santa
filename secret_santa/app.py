#!/usr/bin/env python3
import argparse  # do I need to say more?
import csv  # pretty much only used to check the file
import random  # for the matching
import smtplib  # emails and what not
import sys  # dem error codes


def email(people, matches, email, smtp):
    if email is None:
        email = input("enter email: ")
    if smtp is None:
        smtp = input("enter smtp address: ")

    server = smtplib.SMTP_SSL(smtp, 465)
    try:
        server.login(email, input("input password: "))
    except KeyboardInterrupt:
        print("\nyou little bastard... you have killed me")
        sys.exit(69)  # this is a srmount error (do I care? no)
    except smtplib.SMTPAuthenticationError:
        print("you failed")
        sys.exit(11)

        # TODO You need to send all the emails
    server.sendmail(
        "jeetelongname@gmail.com",
        "jeetelongname@gmail.com",
        "this message is from python")
    server.quit()
    print("well hello themre")


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

            del people[-1]  # delete the lable row
            # start of the matching
            people_copy = people
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
            email(people, matches, args.email, args.smtp)
            sys.exit()
    except IOError:
        print("not valid file path")
        sys.exit(2)
