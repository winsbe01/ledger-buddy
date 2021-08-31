from mail import IMAPClient
from config import config
from struc import Message, Entry
from proc import process_message
from filters import apply_filters


def parse_field_from_header(header, field):
    header_lines = header.decode().splitlines()
    for line in header_lines:
        if line.startswith(f"{field}:"):
            return ":".join(line.split(":")[1:])
    return None


def parse_body(body):
    return body.decode().replace("=\r\n", "")


def assemble_message(raw_header, raw_body):
    subject = parse_field_from_header(raw_header, "Subject")
    from_address = parse_field_from_header(raw_header, "From")
    body = parse_body(raw_body)
    return Message(subject, from_address, body)


def main():
    client = IMAPClient(config["username"], config["password"], config["server"], config["source"])

    entry_list = []

    message_ids = client.get_all_message_ids()
    for message_id in message_ids:
        header, body = client.get_message(message_id)

        message = assemble_message(header, body)
        merchant_name, transaction = process_message(message)
        if transaction is not None:
            merchant = apply_filters(merchant_name)
            entry = Entry(merchant, transaction)
            entry_list.append(entry)

    print(entry_list)


if __name__ == "__main__":
    main()
