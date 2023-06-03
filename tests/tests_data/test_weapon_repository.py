#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model import *
from model import ItemType, DamageType, WeaponType, ItemRarity


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestWeaponRepository(unittest.TestCase):

    data: Db = None
    repository: WeaponsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = WeaponsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_item(self) -> Item:
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
                'infix_upgrade': None
            }
        }

        return Item(data)

    def _assert_weapon(self, db_weapon: Item, weapon: Item):
        self.assertIsNotNone(db_weapon)
        self.assertEqual(weapon.type, db_weapon.type)
        self.assertEqual(weapon.chat_link, db_weapon.chat_link)
        self.assertEqual(weapon.name, db_weapon.name)
        self.assertEqual(weapon.icon, db_weapon.icon)
        self.assertEqual(weapon.description, db_weapon.description)
        self.assertEqual(weapon.rarity, db_weapon.rarity)
        self.assertEqual(weapon.details.type, db_weapon.details.type)
        self.assertEqual(weapon.details.damage_type,
                         db_weapon.details.damage_type)
        self.assertEqual(weapon.details.attribute_adjustment,
                         db_weapon.details.attribute_adjustment)
        self.assertEqual(weapon.details.infix_upgrade,
                         db_weapon.details.infix_upgrade)

    def test_save_weapon(self):
        # given
        weapon = self._build_item()

        # when
        self.repository.save_weapon(weapon)

        # then
        self.assertIsNone(None, "Check that save does not throw")

    def test_get_weapon(self):
        # given
        weapon = self._build_item()
        self.repository.save_weapon(weapon)

        # when
        weapons = self.repository.get_weapon()

        # then
        self.assertIsNotNone(weapons)
        self.assertEqual(len(weapons), 1)

        db_weapon = weapons[0]
        self._assert_weapon(db_weapon, weapon)

    def test_get_weapon_by_type(self):
        # given
        weapon = self._build_item()
        self.repository.save_weapon(weapon)

        # when
        self.assertIsNone(
            self.repository.get_weapon(type=WeaponType.Axe))
        db_weapon = self.repository.get_weapon(type=WeaponType.Dagger)

        # then
        self._assert_weapon(db_weapon, weapon)

    def test_delete_weapons(self):
        # given
        weapon = self._build_item()
        self.repository.save_weapon(weapon)

        # when
        self.repository.delete_weapon()
        db_weapon = self.repository.get_weapon()

        # then
        self.assertListEqual(db_weapon, [])

    def test_delete_weapon_by_type(self):
        # given
        weapon = self._build_item()
        self.repository.save_weapon(weapon)

        # when
        self.repository.delete_weapon(type=WeaponType.Dagger)
        db_weapon = self.repository.get_weapon()

        # then
        self.assertListEqual(db_weapon, [])
