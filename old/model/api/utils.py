#!/usr/bin/env python

def get_or_none(key: str, data: dict = None):
    if (data is not None):
        if key in data:
            return data[key]

    return None


def get_list_or_empty(key: str, data: dict = None) -> list:
    l = get_or_none(key, data)
    return l if l is not None else []


def get_dict_or_empty(key: str, data: dict = None) -> dict:
    l = get_or_none(key, data)
    return l if l is not None else {}
