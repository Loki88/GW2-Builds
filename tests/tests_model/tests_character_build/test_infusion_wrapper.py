#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import InfusionWrapper
from model.enums import Attribute, ItemType, ItemRarity, UpgradeComponentType, UpgradeComponentFlags, InfusionFlag,\
    WeaponType, DamageType


class TestInfusionWrapper(unittest.TestCase):

    def _build_weapon(self, flag: InfusionFlag = InfusionFlag.Infusion, slots: int = 1) -> Item:
        data = {
            'id': 1,
            'chat_link': '[abcde1]',
            'name': 'Tet',
            'icon': 'test',
            'description': 'test',
            'type': ItemType.Weapon.name,
            'rarity': ItemRarity.Legendary.name,
            'details': {
                'type': WeaponType.Dagger.name,
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
                ]
            }
        }

        return Item(data)

    def _build_infusion(self, id: int = 1) -> Item:
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

    def _assert_weapon(self, wrapped_weapon: Item, weapon: Item):
        self.assertIsNotNone(wrapped_weapon)
        self.assertEqual(weapon.type, wrapped_weapon.type)
        self.assertEqual(weapon.chat_link, wrapped_weapon.chat_link)
        self.assertEqual(weapon.name, wrapped_weapon.name)
        self.assertEqual(weapon.icon, wrapped_weapon.icon)
        self.assertEqual(weapon.description, wrapped_weapon.description)
        self.assertEqual(weapon.rarity, wrapped_weapon.rarity)
        self.assertEqual(weapon.details.type, wrapped_weapon.details.type)
        self.assertEqual(weapon.details.damage_type,
                         wrapped_weapon.details.damage_type)
        self.assertEqual(weapon.details.attribute_adjustment,
                         wrapped_weapon.details.attribute_adjustment)
        self.assertEqual(weapon.details.infix_upgrade,
                         wrapped_weapon.details.infix_upgrade)
        
    def _assert_infusion(self, wrapped_infusion: Item, infusion: Item):
        self.assertIsNotNone(wrapped_infusion)
        self.assertEqual(infusion.type, wrapped_infusion.type)
        self.assertEqual(infusion.chat_link, wrapped_infusion.chat_link)
        self.assertEqual(infusion.name, wrapped_infusion.name)
        self.assertEqual(infusion.icon, wrapped_infusion.icon)
        self.assertEqual(infusion.description, wrapped_infusion.description)
        self.assertEqual(infusion.rarity, wrapped_infusion.rarity)
        self.assertEqual(infusion.details.type, wrapped_infusion.details.type)
        self.assertEqual(infusion.details.infix_upgrade.id,
                         wrapped_infusion.details.infix_upgrade.id)
        self.assertListEqual(infusion.details.flags,
                             wrapped_infusion.details.flags)
        self.assertListEqual(infusion.details.infusion_upgrade_flags,
                             wrapped_infusion.details.infusion_upgrade_flags)

    def test_access_fields(self):
        # given
        item: Item = self._build_weapon()
        
        # when
        wrapper: InfusionWrapper = InfusionWrapper(item)

        # then
        self._assert_weapon(wrapper, item)
        self.assertEqual(wrapper.infusion_slots, 1)

    def test_set_infusion(self):
        # given
        item: Item = self._build_weapon()
        wrapper: InfusionWrapper = InfusionWrapper(item)
        infusion: Item = self._build_infusion()
        
        # when
        wrapper.set_infusion(infusion, 0)

        # then
        self._assert_weapon(wrapper, item)
        self._assert_infusion(wrapper.get_infusions()[0], infusion)

    def test_set_multiple_infusion(self):
        # given
        item: Item = self._build_weapon(slots=2)
        wrapper: InfusionWrapper = InfusionWrapper(item)
        infusion1: Item = self._build_infusion(id=1)
        infusion2: Item = self._build_infusion(id=2)
        
        # when
        wrapper.set_infusion(infusion1, 0)
        wrapper.set_infusion(infusion2, 1)

        # then
        self._assert_weapon(wrapper, item)
        infusions = wrapper.get_infusions()
        self._assert_infusion(infusions[0], infusion1)
        self._assert_infusion(infusions[1], infusion2)
