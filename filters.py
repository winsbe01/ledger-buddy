import yaml
import re
import cleansers
from struc import Merchant


def load_filters():
    with open("filters.yml", "r") as fil:
        yobj = yaml.safe_load(fil.read())
    return yobj


def apply_filter(f, in_str):
    r = re.compile(f["match"])
    success = r.match(in_str)
    if success != None:
        fixed = r.sub(f["replace"], in_str)
        if "cleanser" in f and getattr(cleansers, f["cleanser"]) is not None:
            fixed = getattr(cleansers, f["cleanser"])(fixed)
        ret = Merchant(fixed, f["category"])
    else:
        ret = None

    return ret

def apply_filters(in_str):
    filter_map = load_filters()
    for name, f in filter_map.items():
        out = apply_filter(f, in_str)
        if type(out) is Merchant:
            return out
    return None

