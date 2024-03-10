#!/usr/bin/env python


def flatten(list_of_lists: list) -> list:
    return [item for sublist in list_of_lists for item in sublist]


def no_duplicates(list_with_duplicates: list) -> list:
    return list(dict.fromkeys(list_with_duplicates))


def partition(lst: list, chunks: int):
    for i in range(0, len(lst), chunks):
        yield lst[i:i + chunks]
