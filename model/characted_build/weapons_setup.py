#!/usr/bin/env python

from enum import Enum
from model.api import Item
from model.enums import WeaponType, ArmorWeight, ItemType,\
    OneHandedMainHandWeaponType, OneHandedOffHandWeaponType, TwoHandedWeaponType
from .wrapper import InfusionWrapper, SigilWrapper


class WeaponsSet():
    ALLOWED_TYPES = OneHandedMainHandWeaponType._member_names_ +\
        OneHandedOffHandWeaponType._member_names_ +\
        TwoHandedWeaponType._member_names_

    ALLOWED_MAIN_HAND = OneHandedMainHandWeaponType._member_names_ +\
        TwoHandedWeaponType._member_names_

    ALLOWED_OFF_HAND = OneHandedMainHandWeaponType._member_names_ +\
        OneHandedOffHandWeaponType._member_names_

    def __init__(self, main_hand: Item = None, off_hand: Item = None):
        super().__init__()

        if (main_hand is not None and self.is_allowed_main_hand(main_hand)):
            self.main_hand = main_hand

        if (off_hand is not None and self.is_allowed_off_hand(off_hand)):
            if (self.is_compatible_with_main_hand(off_hand)):
                self.main_hand = main_hand
            else:
                raise ValueError("off_hand not compatible with main_hand")

    def is_allowed_main_hand(self, main_hand: Item) -> bool:
        if (main_hand.type == ItemType.Weapon):
            main_hand_type_name = main_hand.details.type.name
            if (main_hand_type_name in WeaponsSet.ALLOWED_MAIN_HAND):
                return True
            else:
                raise ValueError(main_hand_type_name)
        else:
            raise ValueError(main_hand)

    def is_allowed_off_hand(self, off_hand: str) -> bool:
        if (off_hand.type == ItemType.Weapon):
            off_hand_type_name = off_hand.details.type.name
            if (off_hand_type_name in WeaponsSet.ALLOWED_OFF_HAND):
                return True
            else:
                raise ValueError(off_hand_type_name)
        else:
            raise ValueError(off_hand)

    def is_compatible_with_main_hand(self, off_hand: str) -> bool:
        if (self.main_hand is None):
            return True
        else:
            return self.main_hand.details.type.name not in TwoHandedWeaponType._member_names_

    def is_compatible_with_off_hand(self, main_hand: str) -> bool:
        if (self.off_hand is None):
            return True
        else:
            return main_hand.details.type.name not in TwoHandedWeaponType._member_names_

    def set_main_hand(self, main_hand: Item):
        if (self.is_allowed_main_hand(main_hand)):
            if (not self.is_compatible_with_off_hand(main_hand)):
                self.off_hand = None
            self.main_hand = main_hand
        else:
            raise ValueError(main_hand)

    def set_off_hand(self, off_hand: Item):
        if (self.is_allowed_off_hand(off_hand)):
            if (self.is_compatible_with_main_hand(off_hand)):
                self.off_hand = off_hand
            else:
                raise ValueError("off_hand not compatible with main_hand")
        else:
            raise ValueError(off_hand)

    def _is_two_handed(self, item: Item):
        return item is not None and item.details.type.name in TwoHandedWeaponType._member_names_

    def get_weapons(self) -> Item | tuple[Item, Item]:
        two_handed = self._is_two_handed(self.main_hand) or self._is_two_handed(self.off_hand)

        if (two_handed):
            return self.main_hand if self.main_hand is not None else self.off_hand
        else:
            return (self.main_hand, self.off_hand)


class WeaponsSetup():

    class WeaponsSetId(Enum):
        SET_1: 1
        SET_2: 2

    def __init__(self):
        super().__init__()
        self.weapons_sets = dict.fromkeys(WeaponsSetup.WeaponsSetId._member_names_, WeaponsSet())

    def set_weapons(self, set: WeaponsSetId, main_hand: Item = None, off_hand: Item = None):
        self.weapons_sets[set].set_main_hand(main_hand)
        self.weapons_sets[set].set_off_hand(off_hand)

    def get_weapons(self, set: WeaponsSetId) -> Item | tuple[Item, Item]:
        return self.weapons_sets[set].get_weapons()
