#!/usr/bin/env python

from persistent import Persistent
from model.api import Item
from model.enums import InfusionFlag, ItemType, UpgradeComponentType
from .item_wrapper import ItemWrapper


class InfusionWrapper(ItemWrapper):

    def __init__(self, item: Item) -> None:
        super().__init__(item, attributes=['infusion_slots'], list_attributes=['infusions'])
        if (InfusionWrapper.supports(item)):
            self.infusion_slots = len([x for x in item.details.infusion_slots if InfusionFlag.Infusion in x.flags])
            self.infusions = [None for _ in range(self.infusion_slots)]
        else:
            raise ValueError(item)

    @staticmethod
    def supports(item: Item) -> bool:
        try:
            return len([x for x in item.details.infusion_slots if InfusionFlag.Infusion in x.flags]) > 0
        except AttributeError:
            return False

    def _held_component(self) -> UpgradeComponentType:
        return UpgradeComponentType.Default

    def _test_list(self, items: list[Item]):
        for item in items:
            self._test_single(item)

    def _test_single(self, item: Item):
        if (item.type != ItemType.UpgradeComponent or
            item.details.type != UpgradeComponentType.Default or
                InfusionFlag.Infusion not in item.details.infusion_upgrade_flags):

            raise ValueError(item)

    def set_infusion(self, infusion: Item | list[Item], slot: int = None):
        if (slot is None):
            if (isinstance(infusion, list)):
                self._test_list(infusion)
                self.infusions = [x for x in infusion]
            else:
                raise ValueError(infusion)
        else:
            if (isinstance(infusion, Item)):
                self._test_single(infusion)
                self.infusions[slot] = infusion
            else:
                raise ValueError(infusion)

    def get_infusions(self, slot: int = None) -> Item | list[Item]:
        if (slot is None):
            return [x for x in self.infusions]
        else:
            if (slot < self.infusion_slots):
                return self.infusions[slot]
            else:
                raise ValueError(slot)

    def remove_infusion(self, slot: int = None):
        if (slot is None):
            self.infusions = [None for _ in range(self.infusion_slots)]
        else:
            if (slot < self.infusion_slots):
                self.infusions[slot] = None
            else:
                raise ValueError(slot)

    def upgrade(self, upgrade: Item | list[Item], slot: int = None):
        if (upgrade == self._held_component()):
            self.set_infusion(upgrade, slot)
        else:
            try:
                self.item.upgrade(upgrade, slot)
            except BaseException:
                raise ValueError(upgrade)
