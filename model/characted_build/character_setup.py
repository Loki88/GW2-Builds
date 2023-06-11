#!/usr/bin/env python

from .armor_setup import ArmorSetup
from .trinket_setup import TrinketSetup
from .weapons_setup import WeaponsSetup
from .back_setup import BackSetup
from .consumables_setup import ConsumablesSetup

from model.api import Profession, Item
from model.enums import ArmorWeight, LightProfessions, MediumProfessions, HeavyProfessions, ArmorType


class CharacterSetup:

    def __init__(self, profession: Profession):
        self.profession = profession
        self.armor_setup = ArmorSetup(self._get_weight(profession.name))
        self.weapon_setup = WeaponsSetup()
        self.trinket_setup = TrinketSetup()
        self.back_setup = BackSetup()
        self.consumables_setup = ConsumablesSetup()

    def _get_weight(self, profession_name: str) -> ArmorWeight:
        if (profession_name in LightProfessions._member_names_):
            return ArmorWeight.Light
        elif (profession_name in MediumProfessions._member_names_):
            return ArmorWeight.Medium
        elif (profession_name in HeavyProfessions._member_names_):
            return ArmorWeight.Heavy
        else:
            raise ValueError(profession_name)

    def add_armor(self, armor: Item):
        self.armor_setup.set_armor_piece(armor)

    def get_armor(self, type: ArmorType) -> Item | None:
        return self.armor_setup.get_armor_piece(type)

    def add_weapon(self, set: WeaponsSetup.WeaponsSetId, main: Item = None, off: Item = None):
        self.weapon_setup.set_weapons(set, main, off)

    def get_weapon_set(self, set: WeaponsSetup.WeaponsSetId) -> Item | tuple[Item, Item]:
        return self.weapon_setup.get_weapons(set)

    def add_accessory(self, slot: TrinketSetup.Slot, item: Item):
        self.trinket_setup.set_accessory(slot, item)

    def get_accessory(self, slot: TrinketSetup.Slot) -> Item | None:
        return self.trinket_setup.get_accessory(slot)

    def add_ring(self, slot: TrinketSetup.Slot, item: Item):
        self.trinket_setup.set_ring(slot, item)

    def get_ring(self, slot: TrinketSetup.Slot) -> Item | None:
        return self.trinket_setup.get_ring(slot)

    def add_amulet(self, item: Item):
        self.trinket_setup.set_amulet(item)

    def get_amulet(self) -> Item | None:
        return self.trinket_setup.get_amulet()

    def add_back(self, item: Item):
        self.back_setup.set_back(item)

    def get_back(self) -> Item | None:
        return self.back_setup.get_back()

    def set_food(self, item: Item):
        self.consumables_setup.set_food(item)

    def get_food(self) -> Item | None:
        return self.consumables_setup.get_food()

    def set_utility(self, item: Item):
        self.consumables_setup.set_utility(item)

    def get_utility(self) -> Item | None:
        return self.consumables_setup.get_utility()
