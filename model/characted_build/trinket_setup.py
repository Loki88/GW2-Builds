#!/usr/bin/env python

from enum import Enum
from model.api import Item
from model.enums import TrinketType, ItemType


class TrinketSetup():

    class Slot(Enum):
        SLOT_1 = 0
        SLOT_2 = 1
    

    def __init__(self):
        super().__init__()
        self.amulet = None
        self.rings = (None, None)
        self.accessories = (None, None)

    def set_amulet(self, item: Item):
        if (item.type == ItemType.Trinket):
            if (item.details.type == TrinketType.Amulet):
                self.amulet = item
            else:
                raise ValueError(item.details.type)
        else:
            raise ValueError(item.type)

    def set_ring(self, slot: Slot, item: Item):
        if (item.type == ItemType.Trinket):
            if (item.details.type == TrinketType.Ring):
                self.rings[slot] = item
            else:
                raise ValueError(item.details.type)
        else:
            raise ValueError(item.type)

    def set_accessory(self, slot: Slot, item: Item):
        if (item.type == ItemType.Trinket):
            if (item.details.type == TrinketType.Accessory):
                self.accessories[slot] = item
            else:
                raise ValueError(item.details.type)
        else:
            raise ValueError(item.type)
        