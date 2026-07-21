"""Utility helpers with mixed quality for multi-file review demos."""

def fetch_user(id):
    users = {1: "Alice", 2: "Bob"}
    return users[id]  # KeyError if id missing


def parse_int(value):
    try:
        return int(value)
    except:
        return -1  # Bare except swallows all errors


def merge_dicts(a, b):
    a.update(b)
    return a  # Mutates input in place — may surprise callers
