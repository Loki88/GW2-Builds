#!/usr/bin/env python

from model.api import Item
from model.enums import ItemType, UpgradeComponentType
from .item_wrapper import ItemWrapper


class RuneWrapper(ItemWrapper):

    def __init__(self, item: Item) -> None:
        super().__init__(item, attributes=['rune'])
        if (RuneWrapper.supports(item)):
            self.rune = None
        else:
            raise ValueError(item)

    @staticmethod
    def supports(item: Item) -> bool:
        return item.type == ItemType.Armor

    def _held_component(self) -> UpgradeComponentType:
        return UpgradeComponentType.Rune

    def set_rune(self, rune: Item):
        if (rune.type == ItemType.UpgradeComponent and rune.details.type == UpgradeComponentType.Rune):
            self.rune = rune

    def get_rune(self) -> Item | None:
        return self.rune

    def remove_rune(self):
        self.rune = None

    def upgrade(self, upgrade: Item | list[Item], slot: int = None):
        if (upgrade == self._held_component()):
            self.set_rune(upgrade)
        else:
            try:
                self.item.upgrade(upgrade, slot)
            except BaseException:
                raise ValueError(upgrade)
