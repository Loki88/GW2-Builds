#!/usr/bin/env python

import persistent
import persistent.list
from model import InfusionFlag, ItemType, ItemRarity, Attribute, ArmorType, ArmorWeight, TrinketType, ConsumableType, UpgradeComponentType, UpgradeComponentFlags


class InfusionSlot(persistent.Persistent):

    def __init__(self, item_id: int, flags: list[InfusionFlag] = None) -> None:
        super().__init__()
        self.flags = flags
        self.item_id = item_id


class InfixAttributeBonus(persistent.Persistent):

    def __init__(self, attribute: Attribute, modifier: float) -> None:
        self.attribute = attribute
        self.modifier = modifier


class InfixBuff(persistent.Persistent):

    def __init__(self, skill_id: int, description: str) -> None:
        self.skill_id = skill_id
        self.description = description


class InfixUpgrade:
    id: int
    attributes: list[InfixAttributeBonus]
    buff: InfixBuff

    def __init__(self, id: int, attributes: list[InfixAttributeBonus], buff: InfixBuff) -> None:
        self.id = id
        self.buff = buff
        self.attributes = attributes


class ItemDetail(persistent.Persistent):

    def _get_infix_upgrade(self, id: int, attributes: list[InfixAttributeBonus], buff: InfixBuff) -> InfixUpgrade | None:
        return InfixUpgrade(id, attributes, buff)


class Item(persistent.Persistent):

    def __init__(self, id: int, chat_link: str, name: str, icon: str, description: str, type: ItemType, rarity: ItemRarity, details: ItemDetail | None) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.chat_link = chat_link
        self.type = type
        self.rarity = rarity
        self.details = details


class StatsSelectableItem(ItemDetail):

    def __init__(self, attribute_adjustment: float, infix_upgrade: InfixUpgrade | None) -> None:
        self.attribute_adjustment = attribute_adjustment
        self.infix_upgrade = infix_upgrade
        self.stat_choices = persistent.list.PersistentList()
        self.infusion_slots = persistent.list.PersistentList()

    def add_infusion_slot(self, infusion_slot: InfusionSlot):
        self.infusion_slots.append(infusion_slot)

    def add_stat_choiche(self, stat_choice: int):
        self.stat_choices.append(stat_choice)


class ArmorDetail(StatsSelectableItem):

    def __init__(self, type: ArmorType, weight_class: ArmorWeight, defense: int, attribute_adjustment: float,
                 infix_upgrade: InfixUpgrade | None) -> None:
        super().__init__(attribute_adjustment=attribute_adjustment, infix_upgrade=infix_upgrade)
        self.type = type
        self.weight_class = weight_class
        self.defense = defense


class BackDetail(StatsSelectableItem):

    def __init__(self, attribute_adjustment: float, infix_upgrade: InfixUpgrade | None) -> None:
        super().__init__(attribute_adjustment=attribute_adjustment, infix_upgrade=infix_upgrade)


class TrinketDetail(StatsSelectableItem):

    def __init__(self, type: TrinketType, attribute_adjustment: float, infix_upgrade: InfixUpgrade | None) -> None:
        super().__init__(attribute_adjustment=attribute_adjustment, infix_upgrade=infix_upgrade)
        self.type = type


class UpgradeComponentDetail(ItemDetail):
    type: UpgradeComponentType
    flags: list[UpgradeComponentFlags]
    infusion_upgrade_flags: list[InfusionFlag]
    infix_upgrade: InfixUpgrade | None
    bonuses: list[str]

    def __init__(self, type: UpgradeComponentType, infix_upgrade: InfixUpgrade = None) -> None:
        self.type = type
        self.infix_upgrade = infix_upgrade

        self.flags = persistent.list.PersistentList()
        self.infusion_upgrade_flags = persistent.list.PersistentList()
        self.bonuses = persistent.list.PersistentList()

    def add_flag(self, flag: UpgradeComponentFlags):
        if (flag not in self.flags):
            self.flags.append(flag)

    def add_infusion_upgrade_flag(self, flag: InfusionFlag):
        if (flag not in self.infusion_upgrade_flags):
            self.infusion_upgrade_flags.append(flag)

    def add_bonus(self, bonus: str):
        if (bonus not in self.bonuses):
            self.bonuses.append(bonus)


class ConsumableDetail(ItemDetail):

    def __init__(self, type: ConsumableType, description: str, duration_ms: int,
                 recipe_id: int, apply_count: int, name: str, icon: str) -> None:
        self.type = type
        self.description = description
        self.duration_ms = duration_ms
        self.recipe_id = recipe_id
        self.apply_count = apply_count
        self.name = name
        self.icon = icon

        self.extra_recipe_ids = persistent.list.PersistentList()

    def add_extra_recipe(self, id: int):
        if (id not in self.extra_recipe_ids):
            self.extra_recipe_ids.append(id)


DETAILS_DICT = {
    ItemType.Armor: ArmorDetail,
    ItemType.Back: BackDetail,
    ItemType.Trinket: TrinketDetail,
    ItemType.Consumable: ConsumableDetail,
    ItemType.UpgradeComponent: UpgradeComponentDetail
}


def get_item_details(item_type: ItemType, **kwargs) -> ItemDetail | None:
    constructor = DETAILS_DICT[item_type]
    return constructor(kwargs)
