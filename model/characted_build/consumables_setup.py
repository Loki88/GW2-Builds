#!/usr/bin/env python

from model.api import Item
from model.enums import ItemType, ConsumableType


class ConsumablesSetup():

    def __init__(self):
        self.food = None
        self.utility = None

    def set_food(self, item: Item):
        if (item.type == ItemType.Consumable and item.details.type == ConsumableType.Food):
            self.food = item
        else:
            raise ValueError(item)

    def get_food(self) -> Item | None:
        return self.food

    def set_utility(self, item: Item):
        if (item.type == ItemType.Consumable and item.details.type == ConsumableType.Utility):
            self.utility = item
        else:
            raise ValueError(item)

    def get_utility(self) -> Item | None:
        return self.utility
