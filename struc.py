from collections import namedtuple

Message = namedtuple("Message", ["subject", "from_address", "body"])
Transaction = namedtuple("Transaction", ["amount", "txndate", "account"])
