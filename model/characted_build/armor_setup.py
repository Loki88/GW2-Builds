#!/usr/bin/env python

from model.api import Item
from model.enums import ArmorType, ArmorWeight, ItemType
from .wrapper import InfusionWrapper, RuneWrapper

class ArmorSetup():

    def __init__(self, weight: ArmorWeight):
        super().__init__()
        self.weight = weight
        self.armor = dict.fromkeys(ArmorType._member_names_, None)

    def set_armor_piece(self, type: ArmorType, item: Item):
        if (item.type == ItemType.Armor):
            if (item.details.weight_class == self.weight):
                wrapped_item = item
                if(InfusionWrapper.supports(item)):
                    wrapped_item = InfusionWrapper(item)
                if(RuneWrapper.supports(item)):
                    wrapped_item = RuneWrapper(wrapped_item)
                self.armor[item.details.type] = wrapped_item
            else:
                raise ValueError(item, self.weight)
        else:
            raise ValueError(item)
