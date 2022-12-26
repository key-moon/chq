from typing import Optional, Tuple

def parse_chall_name(name: str) -> Tuple[Optional[str], Optional[str]]:
    if name is None:
        return (None, None)
    splitted = name.split("/")
    if len(splitted) != 1:
        if 2 < len(splitted):
            raise Exception("name must be in the form of '([^/]+/)[^/]+'")
        return (splitted[0], splitted[1])
    return (None, splitted[0])

def parse_dest_name(name: str) -> Tuple[Optional[str], Optional[str]]:
    if name is None:
        return (None, None)
    splitted = name.split("/")
    if len(splitted) != 1:
        if 2 < len(splitted):
            raise Exception("name must be in the form of '([^/]+/)[^/]+'")
        return (splitted[0], splitted[1])
    return (splitted[0], None)

