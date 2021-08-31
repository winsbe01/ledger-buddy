from mail import IMAPClient
from config import config
from struc import Message
from proc import process_message


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

    message_ids = client.get_all_message_ids()
    for message_id in message_ids:
        header, body = client.get_message(message_id)

        message = assemble_message(header, body)
        merchant_name, transaction = process_message(message)
        print(merchant_name, transaction)


if __name__ == "__main__":
    main()
