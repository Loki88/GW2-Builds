#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import RuneWrapper
from model.enums import Attribute, ItemType, ItemRarity, UpgradeComponentType, UpgradeComponentFlags, InfusionFlag,\
    ArmorType, ArmorWeight


class TestRuneWrapper(unittest.TestCase):

    def _build_armor(self) -> Item:
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

    def _build_rune(self) -> Item:
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

    def _assert_rune(self, db_rune: Item, rune: Item):
        self.assertIsNotNone(db_rune)
        self.assertEqual(rune.type, db_rune.type)
        self.assertEqual(rune.chat_link, db_rune.chat_link)
        self.assertEqual(rune.name, db_rune.name)
        self.assertEqual(rune.icon, db_rune.icon)
        self.assertEqual(rune.description, db_rune.description)
        self.assertEqual(rune.rarity, db_rune.rarity)
        self.assertEqual(rune.details.type, db_rune.details.type)
        self.assertEqual(rune.details.infix_upgrade.id,
                         db_rune.details.infix_upgrade.id)
        self.assertListEqual(rune.details.flags,
                             db_rune.details.flags)
        self.assertListEqual(rune.details.infusion_upgrade_flags,
                             db_rune.details.infusion_upgrade_flags)

    def _assert_armor(self, db_armor: Item, armor: Item):
        self.assertIsNotNone(db_armor)
        self.assertEqual(armor.type, db_armor.type)
        self.assertEqual(armor.chat_link, db_armor.chat_link)
        self.assertEqual(armor.name, db_armor.name)
        self.assertEqual(armor.icon, db_armor.icon)
        self.assertEqual(armor.description, db_armor.description)
        self.assertEqual(armor.rarity, db_armor.rarity)
        self.assertEqual(armor.details.type, db_armor.details.type)
        self.assertEqual(armor.details.weight_class,
                         db_armor.details.weight_class)
        self.assertEqual(armor.details.defense, db_armor.details.defense)
        self.assertEqual(armor.details.attribute_adjustment,
                         db_armor.details.attribute_adjustment)
        self.assertEqual(armor.details.infix_upgrade,
                         db_armor.details.infix_upgrade)
        

    def test_access_fields(self):
        # given
        item: Item = self._build_armor()
        
        # when
        wrapper: RuneWrapper = RuneWrapper(item)

        # then
        self._assert_armor(wrapper, item)

    def test_set_rune(self):
        # given
        item: Item = self._build_armor()
        wrapper: RuneWrapper = RuneWrapper(item)
        rune: Item = self._build_rune()
        
        # when
        wrapper.set_rune(rune)

        # then
        self._assert_armor(wrapper, item)
        self._assert_rune(wrapper.get_rune(), rune)

    