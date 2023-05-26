#!/usr/bin/env python

from .utils import get_or_none, get_list_or_empty
from .enums import ItemType, ItemRarity, ArmorType, ArmorWeight, InfusionFlag, Attribute, TrinketType, UpgradeComponentType, UpgradeComponentFlags, ConsumableType

class InfusionSlot:
    flags: list[InfusionFlag]
    item_id: int
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.flags = [InfusionFlag[x] for x in get_list_or_empty('id', data)]
            self.item_id = get_or_none('item_id', data)

class InfixAttributeBonus:
    attribute: Attribute
    modifier: float
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.attribute = Attribute[get_or_none('attribute', data)]
            self.modifier = get_or_none('modifier', data)

class InfixBuff:
    skill_id: int
    description: str
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.skill_id = get_or_none('skill_id', data)
            self.description = get_or_none('description', data)

class InfixUpgrade:
    id: int
    attributes: list[InfixAttributeBonus]
    buff: InfixBuff
    
    def __init__(self, data: dict) -> None:
        self.id = get_or_none('id')
        self.buff = InfixBuff[get_or_none('buff')]
        self.attributes = [InfixAttributeBonus[x] for x in get_list_or_empty('attributes')]

class ItemDetail:
    
    def _get_infix_upgrade(self, data: dict) -> InfixUpgrade | None:
        if(data is not None):
            return InfixUpgrade(data)
        return None

class ArmorDetail(ItemDetail):
    type: ArmorType
    weight_class: ArmorWeight
    defense: int
    infusion_slots: list[InfusionSlot]
    attribute_adjustment: float
    infix_upgrade: InfixUpgrade | None
    stat_choices: list[int]
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.type = ArmorType[get_or_none('type', data)]
            self.weight_class = ArmorWeight[get_or_none('weight_class', data)]
            self.defense = get_or_none('defense', data)
            self.infusion_slots = [InfusionSlot(x) for x in get_list_or_empty('infusion_slots', data)]
            self.attribute_adjustment = get_or_none('attribute_adjustment', data)
            self.infix_upgrade = self._get_infix_upgrade(get_or_none('infix_upgrade', data))
            self.stat_choices = [int(x) for x in get_list_or_empty('stat_choices', data)]

class BackDetail(ItemDetail):
    infusion_slots: list[InfusionSlot]
    attribute_adjustment: float
    infix_upgrade: InfixUpgrade | None
    stat_choices: list[int]
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.infusion_slots = [InfusionSlot(x) for x in get_list_or_empty('infusion_slots', data)]
            self.attribute_adjustment = get_or_none('attribute_adjustment', data)
            self.infix_upgrade = self._get_infix_upgrade(get_or_none('infix_upgrade', data))
            self.stat_choices = [int(x) for x in get_list_or_empty('stat_choices', data)]

class TrinketDetail(ItemDetail):
    type: TrinketType
    infusion_slots: list[InfusionSlot]
    attribute_adjustment: float
    infix_upgrade: InfixUpgrade | None
    stat_choices: list[int]
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.type = TrinketType[get_or_none('type', data)]
            self.infusion_slots = [InfusionSlot(x) for x in get_list_or_empty('infusion_slots', data)]
            self.attribute_adjustment = get_or_none('attribute_adjustment', data)
            self.infix_upgrade = self._get_infix_upgrade(get_or_none('infix_upgrade', data))
            self.stat_choices = [int(x) for x in get_list_or_empty('stat_choices', data)]

class UpgradeComponentDetail(ItemDetail):
    type: UpgradeComponentType
    flags: list[UpgradeComponentFlags]
    infusion_upgrade_flags: list[InfusionFlag]
    infix_upgrade: InfixUpgrade | None
    bonuses: list[str]
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.type = UpgradeComponentType[get_or_none('type', data)]
            self.flags = [UpgradeComponentFlags[x] for x in get_list_or_empty('flags', data)]
            self.infusion_upgrade_flags = [InfusionFlag[x] for x in get_list_or_empty('infusion_upgrade_flags', data)]
            self.infix_upgrade = self._get_infix_upgrade(get_or_none('infix_upgrade', data))
            self.bonuses = get_list_or_empty('bonuses', data)

class ConsumableDetail(ItemDetail):
    type: ConsumableType
    description: str
    duration_ms: int
    recipe_id: int
    extra_recipe_ids: list[int]
    apply_count: int
    name: str
    icon: str
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.type = ConsumableType[get_or_none('type', data)]
            self.description = get_or_none('description', data)
            self.duration_ms = get_or_none('duration_ms', data)
            self.recipe_id = get_or_none('recipe_id', data)
            self.extra_recipe_ids = get_list_or_empty('extra_recipe_ids', data)
            self.apply_count = get_or_none('apply_count', data)
            self.name = get_or_none('name', data)
            self.icon = get_or_none('icon', data)

DETAILS_DICT = {
    ItemType.Armor: ArmorDetail,
    ItemType.Back: BackDetail,
    ItemType.Trinket: TrinketDetail,
    ItemType.Consumable: ConsumableDetail,
    ItemType.UpgradeComponent: UpgradeComponentDetail
}

def get_item_details(data: dict, item_type: ItemType) -> ItemDetail | None:
    if(data is not None):
        constructor = DETAILS_DICT[item_type]
        return constructor(data)
    return None

class Item:
    id: int
    chat_link: str
    name: str
    icon: str
    description: str
    type: ItemType
    rarity: ItemRarity
    details: ItemDetail
    
    def __init__(self, data: dict = None) -> None:
        if(data is not None):
            self.id = get_or_none('id', data)
            self.name = get_or_none('name', data)
            self.description = get_or_none('description', data)
            self.icon = get_or_none('icon', data)
            self.chat_link = get_or_none('chat_link', data)
            self.type = ItemType[get_or_none('type', data)]
            self.rarity = ItemRarity[get_or_none('rarity', data)]
            self.details = get_item_details(get_or_none('details', data), self.type)
            
            
def filter_item_data(data: dict, filter: dict[ItemType, ItemRarity] = None) -> bool:
    if(filter is None):
        return True
    else:
        type = get_or_none('type', data)
        if(type in ItemType._member_names_):
            item_type = ItemType[type]
            if(item_type in filter):
                rarity_filter = filter[item_type]
                rarity = get_or_none('rarity', data)
                if(rarity in ItemRarity._member_names_):
                    return ItemRarity[rarity] is rarity_filter
        return False
        