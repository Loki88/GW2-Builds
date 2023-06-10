#!/usr/bin/env python

import unittest

from model.api import Item
from model.characted_build import SigilWrapper
from model.enums import Attribute, ItemType, ItemRarity, UpgradeComponentType, UpgradeComponentFlags, InfusionFlag,\
    WeaponType, DamageType


class TestInfusionWrapper(unittest.TestCase):

    def _build_weapon(self, type: WeaponType = WeaponType.Dagger) -> Item:
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
                'sigil_slots': []
            }
        }

        return Item(data)

    def _build_sigil(self, id: int = 1) -> Item:
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

    def _assert_sigil(self, db_sigil: Item, sigil: Item):
        self.assertIsNotNone(db_sigil)
        self.assertEqual(sigil.type, db_sigil.type)
        self.assertEqual(sigil.chat_link, db_sigil.chat_link)
        self.assertEqual(sigil.name, db_sigil.name)
        self.assertEqual(sigil.icon, db_sigil.icon)
        self.assertEqual(sigil.description, db_sigil.description)
        self.assertEqual(sigil.rarity, db_sigil.rarity)
        self.assertEqual(sigil.details.type, db_sigil.details.type)
        self.assertEqual(sigil.details.infix_upgrade.id,
                         db_sigil.details.infix_upgrade.id)
        self.assertListEqual(sigil.details.flags,
                             db_sigil.details.flags)
        self.assertListEqual(sigil.details.infusion_upgrade_flags,
                             db_sigil.details.infusion_upgrade_flags)

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
        
    
    def test_access_fields(self):
        # given
        item: Item = self._build_weapon()
        
        # when
        wrapper: SigilWrapper = SigilWrapper(item)

        # then
        self._assert_weapon(wrapper, item)
        self.assertEqual(wrapper.sigil_slots, 1)

    def test_set_sigil(self):
        # given
        item: Item = self._build_weapon()
        wrapper: SigilWrapper = SigilWrapper(item)
        sigil: Item = self._build_sigil()
        
        # when
        wrapper.set_sigil(sigil, 0)

        # then
        self._assert_weapon(wrapper, item)
        self._assert_sigil(wrapper.get_sigils()[0], sigil)

    def test_set_multiple_sigil(self):
        # given
        item: Item = self._build_weapon(type=WeaponType.LongBow)
        wrapper: SigilWrapper = SigilWrapper(item)
        sigil1: Item = self._build_sigil(id=1)
        sigil2: Item = self._build_sigil(id=2)
        
        # when
        wrapper.set_sigil(sigil1, 0)
        wrapper.set_sigil(sigil2, 1)

        # then
        self._assert_weapon(wrapper, item)
        sigils = wrapper.get_sigils()
        self._assert_sigil(sigils[0], sigil1)
        self._assert_sigil(sigils[1], sigil2)
