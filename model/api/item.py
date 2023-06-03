#!/usr/bin/env python

from abc import ABC
from typing import Callable
from .api_decorator import ApiDecorator
from .utils import get_or_none
from model.enums import *


class InfusionSlot(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['item_id'],
                         list_attributes + ['flags'],
                         dict_attributes,
                         {
                             'flags': lambda x: [InfusionFlag[f] for f in x]
                         }
                         | converters)


class InfixAttributeBonus(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['attribute', 'modifier'],
                         list_attributes,
                         dict_attributes,
                         {
                             'attribute': lambda x: Attribute[x] if x is not None else None
                         }
                         | converters)


class InfixBuff(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['skill_id', 'description'],
                         list_attributes,
                         dict_attributes,
                         converters)


class InfixUpgrade(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'buff'],
                         list_attributes + ['attributes'],
                         dict_attributes,
                         {
                             'attributes': lambda x: [InfixAttributeBonus(a) for a in x],
                             'buff': lambda x: InfixBuff(x) if x is not None else None
                         }
                         | converters)


class ItemDetail(ApiDecorator, ABC):

    def _get_infix_upgrade(self, data: dict) -> InfixUpgrade | None:
        if (data is not None):
            return InfixUpgrade(data)
        return None


class ArmorDetail(ItemDetail):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['type', 'weight_class', 'defense',
                                       'attribute_adjustment', 'infix_upgrade'],
                         list_attributes + ['infusion_slots', 'stat_choices'],
                         dict_attributes,
                         {
                             'type': lambda x: ArmorType[x] if x is not None else None,
                             'weight_class': lambda x: ArmorWeight[x] if x is not None else None,
                             'infusion_slots': lambda x: [InfusionSlot(s) for s in x],
                             'infix_upgrade': lambda x: self._get_infix_upgrade(x) if x is not None else None,
                             'stat_choices': lambda x: [int(s) for s in x],
                         }
                         | converters)


class BackDetail(ItemDetail):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes +
                         ['attribute_adjustment', 'infix_upgrade'],
                         list_attributes + ['infusion_slots', 'stat_choices'],
                         dict_attributes,
                         {
                             'infusion_slots': lambda x: [InfusionSlot(s) for s in x],
                             'infix_upgrade': lambda x: self._get_infix_upgrade(x) if x is not None else None,
                             'stat_choices': lambda x: [int(s) for s in x],
                         }
                         | converters)


class TrinketDetail(ItemDetail):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes +
                         ['type', 'attribute_adjustment', 'infix_upgrade'],
                         list_attributes + ['infusion_slots', 'stat_choices'],
                         dict_attributes,
                         {
                             'type': lambda x: TrinketType[x] if x is not None else None,
                             'infusion_slots': lambda x: [InfusionSlot(s) for s in x],
                             'infix_upgrade': lambda x: self._get_infix_upgrade(x) if x is not None else None,
                             'stat_choices': lambda x: [int(s) for s in x],
                         }
                         | converters)


class UpgradeComponentDetail(ItemDetail):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['type', 'infix_upgrade'],
                         list_attributes +
                         ['flags', 'infusion_upgrade_flags', 'bonuses'],
                         dict_attributes,
                         {
                             'type': lambda x: UpgradeComponentType[x] if x is not None else None,
                             'flags': lambda x: [UpgradeComponentFlags[f] for f in x],
                             'infusion_upgrade_flags': lambda x: [InfusionFlag[f] for f in x],
                             'infix_upgrade': lambda x: self._get_infix_upgrade(x) if x is not None else None,
                             'stat_choices': lambda x: [int(s) for s in x],
                         }
                         | converters)


class ConsumableDetail(ItemDetail):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['type', 'description', 'duration_ms', 'recipe_id',
                                       'apply_count', 'name', 'icon'],
                         list_attributes + ['extra_recipe_ids'],
                         dict_attributes,
                         {
                             'type': lambda x: ConsumableType[x] if x is not None else None
                         }
                         | converters)


class WeaponDetail(ItemDetail):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['type', 'damage_type', 'min_power', 'max_power', 'defense',
                                       'attribute_adjustment', 'infix_upgrade'],
                         list_attributes + ['infusion_slots', 'stat_choices'],
                         dict_attributes,
                         {
                             'type': lambda x: WeaponType[x] if x is not None else None,
                             'damage_type': lambda x: DamageType[x] if x is not None else None,
                             'infusion_slots': lambda x: [InfusionSlot(s) for s in x],
                             'infix_upgrade': lambda x: self._get_infix_upgrade(x) if x is not None else None,
                             'stat_choices': lambda x: [int(s) for s in x],
                         }
                         | converters)


DETAILS_DICT = {
    ItemType.Armor: ArmorDetail,
    ItemType.Back: BackDetail,
    ItemType.Trinket: TrinketDetail,
    ItemType.Consumable: ConsumableDetail,
    ItemType.UpgradeComponent: UpgradeComponentDetail,
    ItemType.Weapon: WeaponDetail
}


def get_item_details(data: dict, item_type: ItemType) -> ItemDetail | None:
    if (data is not None):
        constructor = DETAILS_DICT[item_type]
        return constructor(data)
    return None


class Item(ApiDecorator):

    def __init__(self, data: dict = None,
                 attributes: list[str] = [],
                 list_attributes: list[str] = [],
                 dict_attributes: list[str] = [],
                 converters: dict[str, Callable] = {}) -> None:
        super().__init__(data,
                         attributes + ['id', 'chat_link', 'name', 'icon', 'description',
                                       'type', 'rarity', 'details'],
                         list_attributes,
                         dict_attributes,
                         {
                             'type': lambda x: ItemType[x] if x is not None else None,
                             'rarity': lambda x: ItemRarity[x] if x is not None else None,
                             'details': lambda x: get_item_details(x, self.type) if x is not None else None,
                         }
                         | converters)


def filter_item_data(data: dict, filter: dict[ItemType, ItemRarity] = None) -> bool:
    if (filter is None):
        return True
    else:
        type = get_or_none('type', data)
        if (type in ItemType._member_names_):
            item_type = ItemType[type]
            if (item_type in filter):
                rarity_filter = filter[item_type]
                if rarity_filter is None:
                    return True
                rarity = get_or_none('rarity', data)
                if (rarity in ItemRarity._member_names_):
                    return ItemRarity[rarity] is rarity_filter
        return False
