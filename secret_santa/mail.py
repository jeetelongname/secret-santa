#!/usr/bin/env python3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
import smtplib  # emails and what not
import ssl
import sys


def email_maker(recever_array, sender_array, address, email_location):
    body = """
    hello {sender},

    You have been roped into a secret santa with the rest of your peers
    you will be giving a gift to {recever},

    They live at {address} and you will infact be covering shipping

    Regards ,
    an automated script made by a child
    """
    message = MIMEMultipart("alternate")
    message["Subject"] = "your secret santa allocation"
    message["From"] = address
    message["To"] = recever_array[email_location]
    message.attach(MIMEText
                   (body.format(
                       sender=sender_array[0],  # sender name

                       # recever name
                       recever=recever_array[0] +
                       " " + recever_array[1],

                       # recever address
                       address=recever_array[3] +
                       " " + recever_array[4]
                   ), "plain"))
    return message.as_string()


def bootstrap(people, matches, address, smtp):
    email_location = 2
    # incase the user is dumb and does not provide at run time
    if address is None:
        address = input("enter email: ")
    if smtp is None:
        smtp = input("enter smtp address: ")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp, context=context) as server:
        w = 0  # to do a time out
        # a lot can go wrong at login time thus this bigass (relative)
        # try - except
        while True:
            # we loop until we get somthing either a break or an exit :)
            try:
                # get pass actually includes a sudo like delay
                server.login(address, getpass(
                    prompt="Password (there is a delay): "))
                break
            except KeyboardInterrupt:
                print("\nyou little bastard... you have killed me")
                sys.exit(69)  # this is a srmount error (do I care? no)
            except smtplib.SMTPAuthenticationError:
                # FIXME there is no way to ask for the email again *yet*
                print("\nyou failed")
                continue
            except smtplib.SMTPServerDisconnected:
                # try 5 times and they give up
                w += 1
                if w == 5:
                    print("aigt Im out")
                    sys.exit(103)
                else:
                    print("the server is a bit annoying give it another go")
                    continue
            # except ssl.SSLEOFError:
            #     w += 1
            #     if w == 5:
            #         print("aigt Im out")
            #         sys.exit(103)
            #     else:
            #         print("the server is a bit annoying give it another go")
            #         continue

    # email construction and sending (the out house)
        try:
            confirm = input(
                """ you sure you want to send all of these emails?
                they will fire like a machine gun after this (y/n):\n
                """)
        except KeyboardInterrupt:
            print("\nyou killed me.. You could have just said no...")
            sys.exit(420)

        if confirm == "y":
            for i in matches:
                # sender = people.get(i)
                recever = people.get(matches[i])[email_location]
                server.sendmail(
                    address,  # the user address
                    recever,  # the recever email
                    # the actual *custom* message
                    email_maker(people.get(i),  # array for the sender
                                people.get(matches[i]),  # array for recever
                                address,  # the address all of them are sent on
                                email_location))  # in the arrays
                # sent check (for sanity)
                print("sent to",
                      people.get(i)[0], i, "down!", len(matches) - i, "to go!")
        else:
            print("too bad, we could have made something great here\n")

        server.close()
