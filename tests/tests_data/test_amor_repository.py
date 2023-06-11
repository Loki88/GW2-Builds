#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model import *
from model import ItemType, ItemRarity


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestArmorRepository(unittest.TestCase):

    data: Db = None
    repository: ArmorRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mock_object = ConfigProvider
        mock_object.get_data_dir = Mock(return_value=test_db_dir)
        mock_object.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = ArmorRepository()

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

    def test_save_armor(self):
        # given
        armor = self._build_item()

        # when
        self.repository.save_armor(armor)

    def test_get_armor(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        armors = self.repository.get_armor()

        # then
        self.assertIsNotNone(armors)
        self.assertEqual(len(armors), 1)

        db_armor = armors[0]
        self._assert_armor(db_armor, armor)

    def test_get_armor_by_weight(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.assertListEqual(self.repository.get_armor(
            weight=ArmorWeight.Heavy), [])
        armors = self.repository.get_armor(weight=ArmorWeight.Medium)

        # then
        self.assertIsNotNone(armors)
        self.assertEqual(len(armors), 1)

        db_armor = armors[0]
        self._assert_armor(db_armor, armor)

    def test_get_armor_by_type(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.assertListEqual(
            self.repository.get_armor(type=ArmorType.Gloves), [])
        armors = self.repository.get_armor(type=ArmorType.Boots)

        # then
        self.assertIsNotNone(armors)
        self.assertEqual(len(armors), 1)

        db_armor = armors[0]
        self._assert_armor(db_armor, armor)

    def test_get_armor_by_weight_and_type(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.assertEqual(self.repository.get_armor(
            weight=ArmorWeight.Medium, type=ArmorType.Gloves), None)
        db_armor = self.repository.get_armor(
            weight=ArmorWeight.Medium, type=ArmorType.Boots)

        # then
        self._assert_armor(db_armor, armor)

    def test_delete_armors(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.repository.delete_armor()
        db_armor = self.repository.get_armor()

        # then
        self.assertListEqual(db_armor, [])

    def test_delete_armor_by_weight(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.repository.delete_armor(weight=ArmorWeight.Medium)
        db_armor = self.repository.get_armor()

        # then
        self.assertListEqual(db_armor, [])

    def test_delete_armor_by_type(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.repository.delete_armor(type=ArmorType.Boots)
        db_armor = self.repository.get_armor()

        # then
        self.assertListEqual(db_armor, [])

    def test_delete_armor_by_weight_and_type(self):
        # given
        armor = self._build_item()
        self.repository.save_armor(armor)

        # when
        self.repository.delete_armor(
            weight=ArmorWeight.Medium, type=ArmorType.Boots)
        db_armor = self.repository.get_armor()

        # then
        self.assertListEqual(db_armor, [])
