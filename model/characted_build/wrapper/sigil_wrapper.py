#!/usr/bin/env python

from model.api import Item
from model.enums import ItemType, UpgradeComponentType, TwoHandedWeaponType
from .item_wrapper import ItemWrapper


class SigilWrapper(ItemWrapper):

    def __init__(self, item: Item) -> None:
        super().__init__(item, attributes=['sigil_slots'], list_attributes=['sigils'])
        if (SigilWrapper.supports(item)):
            self.sigil_slots = 2 if item.details.type.name in TwoHandedWeaponType._member_names_ else 1
            self.sigils = [None for _ in range(self.sigil_slots)]
        else:
            raise ValueError(item)

    @staticmethod
    def supports(item: Item) -> bool:
        return item.type == ItemType.Weapon

    def _held_component(self) -> UpgradeComponentType:
        return UpgradeComponentType.Sigil

    def set_sigil(self, sigil: Item | list[Item], slot: int = None):
        if (slot is None):
            if (isinstance(sigil, list)):
                self.sigils = [x for x in sigil]
            else:
                raise ValueError(sigil)
        else:
            if (isinstance(sigil, Item)):
                self.sigils[slot] = sigil
            else:
                raise ValueError(sigil)

    def get_sigils(self, slot: int = None) -> Item | list[Item]:
        if (slot is None):
            return [x for x in self.sigils]
        else:
            if (slot < self.sigil_slots):
                return self.sigils[slot]
            else:
                raise ValueError(slot)

    def remove_sigil(self, slot: int = None):
        if (slot is None):
            self.sigils = [None for _ in range(self.sigil_slots)]
        else:
            if (slot < self.sigil_slots):
                self.sigils[slot] = None
            else:
                raise ValueError(slot)

    def upgrade(self, upgrade: Item | list[Item], slot: int = None):
        if (upgrade == self._held_component()):
            self.set_sigil(upgrade, slot)
        else:
            try:
                self.item.upgrade(upgrade, slot)
            except BaseException:
                raise ValueError(upgrade)
