#!/usr/bin/env python

from model.api import Item
from model.enums import ItemType
from .wrapper import InfusionWrapper, RuneWrapper

class BackSetup():

    def __init__(self):
        super().__init__()
        self.back = None
        
    def set_back(self, item: Item):
        if (item.type == ItemType.Back):
            self.back = item
        else:
            raise ValueError(item)

    def get_back(self) -> Item | None:
        return self.back