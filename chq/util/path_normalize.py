

import string

SEP_CHAR = " -_"
def normalize(name: str):
    res = ""
    for c in name:
        if c in string.ascii_uppercase: c = c.lower()
        if c in SEP_CHAR: c = '-'
        res += c
    return res
