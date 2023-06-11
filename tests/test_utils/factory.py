#!/usr/bin/env python

from model.enums import InfusionFlag, ItemType, ItemRarity, WeaponType, DamageType, UpgradeComponentType,\
    UpgradeComponentFlags, Attribute, ArmorType, ArmorWeight
from model.api import Item


def _build_item(type: ItemType, id: int = 1) -> dict:
    return {
        'id': id,
        'chat_link': '[abcde1]',
        'name': 'Tet',
        'icon': 'test',
        'description': 'test',
        'type': type.name,
        'rarity': ItemRarity.Legendary.name
    }


def _build_upgrade_component(type: UpgradeComponentType, infusion_flag: InfusionFlag = None) -> dict:
    return {
        'details': {
            'type': type.name,
            'infix_upgrade': {
                'id': 1,
                'attributes': [
                    {
                        'attribute': Attribute.ConditionDamage.name,
                        'modifier': 5
                    }
                ],
                'buff': {
                    'skill_id': 5,
                    'description': 'Test'
                }
            },
            'duration_ms': 30000,
            'recipe_id': 1,
            'apply_count': 1,
            'name': 'Test',
            'icon': 'test',
            'bonuses': ['expertise'],
            'flags': [UpgradeComponentFlags.Axe.name],
            'infusion_upgrade_flags': [infusion_flag.name] if infusion_flag is not None else None
        }
    }


def build_weapon(
        id: int = 1,
        flag: InfusionFlag = InfusionFlag.Infusion,
        slots: int = 1,
        type=WeaponType.Dagger) -> Item:
    data = _build_item(ItemType.Weapon, id) |\
        {
            'details': {
                'type': type.name,
                'damage_type': DamageType.Physical.name,
                'min_power': 150,
                'max_power': 500,
                'defense': 140,
                'attribute_adjustment': 356,
                'infix_upgrade': None,
                'infusion_slots': [
                    {
                        'flags': [
                            flag.name
                        ]
                    } for x in range(slots)
                ],
                'sigil_slots': []
            }
    }

    return Item(data)


def build_infusion(id: int = 1) -> Item:
    data = _build_item(ItemType.UpgradeComponent, id) |\
        _build_upgrade_component(UpgradeComponentType.Default, InfusionFlag.Infusion)

    return Item(data)


def build_armor(id: int = 1) -> Item:
    data = _build_item(ItemType.Armor, id) |\
        {
            'details': {
                'type': ArmorType.Boots.name,
                'weight_class': ArmorWeight.Medium.name,
                'defense': 160,
                'attribute_adjustment': 12.4,
                'infix_upgrade': None
            }
    }

    return Item(data)


def build_rune() -> Item:
    data = _build_item(ItemType.UpgradeComponent, id) |\
        _build_upgrade_component(UpgradeComponentType.Rune)

    return Item(data)


def build_sigil(id: int = 1) -> Item:
    data = _build_item(ItemType.UpgradeComponent, id) |\
        _build_upgrade_component(UpgradeComponentType.Sigil)

    return Item(data)
