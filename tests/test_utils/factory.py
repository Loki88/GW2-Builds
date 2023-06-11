#!/usr/bin/env python

from model.enums import InfusionFlag, ItemType, ItemRarity, WeaponType, DamageType, UpgradeComponentType,\
    UpgradeComponentFlags, Attribute, ArmorType, ArmorWeight
from model.api import Item


def build_weapon(flag: InfusionFlag = InfusionFlag.Infusion, slots: int = 1, type=WeaponType.Dagger) -> Item:
    data = {
        'id': 1,
        'chat_link': '[abcde1]',
        'name': 'Tet',
        'icon': 'test',
        'description': 'test',
        'type': ItemType.Weapon.name,
        'rarity': ItemRarity.Legendary.name,
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
    data = {
        'id': id,
        'chat_link': '[abcde1]',
        'name': 'Tet',
        'icon': 'test',
        'description': 'test',
        'type': ItemType.UpgradeComponent.name,
        'rarity': ItemRarity.Legendary.name,
        'details': {
            'type': UpgradeComponentType.Default.name,
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
            'infusion_upgrade_flags': [InfusionFlag.Infusion.name]
        }
    }

    return Item(data)


def build_armor() -> Item:
    data = {
        'id': 1,
        'chat_link': '[abcde1]',
        'name': 'Tet',
        'icon': 'test',
        'description': 'test',
        'type': ItemType.Armor.name,
        'rarity': ItemRarity.Legendary.name,
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
    data = {
        'id': 1,
        'chat_link': '[abcde1]',
        'name': 'Tet',
        'icon': 'test',
        'description': 'test',
        'type': ItemType.UpgradeComponent.name,
        'rarity': ItemRarity.Legendary.name,
        'details': {
            'type': UpgradeComponentType.Rune.name,
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
            'infusion_upgrade_flags': [InfusionFlag.Infusion.name]
        }
    }

    return Item(data)


def build_sigil(id: int = 1) -> Item:
    data = {
        'id': id,
        'chat_link': '[abcde1]',
        'name': 'Tet',
        'icon': 'test',
        'description': 'test',
        'type': ItemType.UpgradeComponent.name,
        'rarity': ItemRarity.Legendary.name,
        'details': {
            'type': UpgradeComponentType.Sigil.name,
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
            'sigil_upgrade_flags': [InfusionFlag.Infusion.name]
        }
    }

    return Item(data)
