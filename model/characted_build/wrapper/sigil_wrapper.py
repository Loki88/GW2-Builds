#!/usr/bin/env python

from model.api import Item

class SigilWrapper(Item):

    def __init__(self, item: Item) -> None:
        self.item = Item