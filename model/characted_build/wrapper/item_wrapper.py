#!/usr/bin/env python

from abc import ABC
from model.api import Item

class ItemWrapper(Item, ABC):

    def __init__(self, item: Item) -> None:
        pass

    