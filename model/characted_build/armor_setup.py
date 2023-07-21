#!/usr/bin/env python

from model.api import Item
from model.enums import ArmorType, ArmorWeight, ItemType


class ArmorSetup():

    def __init__(self, weight: ArmorWeight):
        super().__init__()
        self.weight = weight
        self.armor = dict.fromkeys(ArmorType._member_names_, None)

    def set_armor_piece(self, item: Item):
        if (item.type == ItemType.Armor):
            if (item.details.weight_class == self.weight):
                self.armor[item.details.type] = item
            else:
                raise ValueError(item, self.weight)
        else:
            raise ValueError(item)

    def get_armor_piece(self, type: ArmorType) -> Item | None:
        return self.armor[type]
