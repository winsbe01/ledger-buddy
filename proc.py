from datetime import datetime
from struc import Transaction


def process_message(message):
    merchant_name = message.subject
    transaction = None
    for key, func in process_map.items():
        if key in message.from_address.lower():
            try:
                merchant_name, transaction = func(message)
            except Exception as e:
                print(f"caught an exception: {e}")
    return merchant_name, transaction


def process_chase(message):
    '''
    As of this writing (2021-08-31), Chase alert emails 
    are HTML only, with the data ensconsed in a helltable. 
    I'd rather not write a parser -- I'm a masochist, but 
    even I have limits. Luckily, the subject has most of 
    what we need.

    Subject formatted as such:
        Your {amount} transaction with {merchant_name}
    Best we can do is today's date for the txndate.
    '''

    print("processing chase...")
    subject_split = message.subject.split(" transaction with ")

    amount = "$" + subject_split[0].split("$")[1].strip()
    merchant_name = subject_split[1].strip()
    txndate = datetime.today()

    return merchant_name, Transaction(amount, txndate, "Liabilities:Chase")


def process_discover(message):
    print("processing discover...")
    bodylines = message.body.splitlines()
    amount = merchant_name = date_string = None
    for line in bodylines:
        line = line.replace("::", ":")
        if line.startswith("Transaction Date:"):
            date_string = ":".join(line.split(":")[1:]).strip()
        elif line.startswith("Merchant:"):
            merchant_name = ":".join(line.split(":")[1:]).strip()
        elif line.startswith("Amount:"):
            amount = ":".join(line.split(":")[1:]).strip()

    txndate = datetime.strptime(date_string, "%B %d, %Y")

    return merchant_name, Transaction(amount, txndate, "Liabilities:Discover")


def process_privacy(message):
    print("processing privacy...")
    bodylines = message.body.splitlines()
    amount = merchant_name = None
    txndate = datetime.today()

    for line in bodylines:
        if line.startswith("There is a new authorization"):
            merchant_name = line.split("'")[3]
            amount = "$" + line.split("$")[1].split(" ")[0]
            break

    return merchant_name, Transaction(amount, txndate, "Assets:BofA Checking")


process_map = {"chase": process_chase,
                "discover": process_discover,
                "privacy": process_privacy}
