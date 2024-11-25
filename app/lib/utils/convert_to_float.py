import re

def convert_to_float(s):
    s = re.sub(r'[^0-9.]', '', s)
    f = round(float(s), 2)
    return f
