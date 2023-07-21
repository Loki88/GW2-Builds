#!/usr/bin/env python

from model.api import Item, ItemStats
from model.enums import ItemType, UpgradeComponentType
from .item_wrapper import ItemWrapper


class StatsWrapper(ItemWrapper):

    def __init__(self, item: Item) -> None:
        super().__init__(item, attributes=['stats'])
        if (StatsWrapper.supports(item)):
            self.stats = None
        else:
            raise ValueError(item)

    @staticmethod
    def supports(item: Item) -> bool:
        try:
            return item.details.stat_choices is not None
        except AttributeError:
            return False

    def set_stats(self, stats: ItemStats):
        self.stats = stats

    def get_stats(self) -> Item | None:
        return self.stats

    def upgrade(self, upgrade: Item | list[Item], slot: int = None):
        if (upgrade == self._held_component()):
            self.set_rune(upgrade)
        else:
            try:
                self.item.upgrade(upgrade, slot)
            except BaseException:
                raise ValueError(upgrade)
