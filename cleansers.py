def fix_case(in_str):
    return " ".join([s[0].upper() + s[1:].lower() for s in in_str.split(" ")])
