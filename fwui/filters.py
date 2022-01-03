import re


def active(path, pattern, type="active"):
    if re.search(pattern, path):
        return type
