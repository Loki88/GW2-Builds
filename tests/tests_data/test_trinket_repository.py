#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model.dao import *
from model import ItemType, ItemRarity, TrinketType


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestTrinketRepository(unittest.TestCase):

    data: Db = None
    repository: TrinketsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = TrinketsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_item(self) -> Item:
        detail = TrinketDetail(type=TrinketType.Accessory,
                               attribute_adjustment=12.4, infix_upgrade=None)
        return Item(id=1, chat_link='[abcde1]', name='Tet', icon='test', description='test', type=ItemType.Trinket, rarity=ItemRarity.Legendary, details=detail)

    def _assert_trinket(self, db_trinket: Item, trinket: Item):
        self.assertIsNotNone(db_trinket)
        self.assertEqual(trinket.type, db_trinket.type)
        self.assertEqual(trinket.chat_link, db_trinket.chat_link)
        self.assertEqual(trinket.name, db_trinket.name)
        self.assertEqual(trinket.icon, db_trinket.icon)
        self.assertEqual(trinket.description, db_trinket.description)
        self.assertEqual(trinket.rarity, db_trinket.rarity)
        self.assertEqual(trinket.details.type, db_trinket.details.type)
        self.assertEqual(trinket.details.attribute_adjustment,
                         db_trinket.details.attribute_adjustment)
        self.assertEqual(trinket.details.infix_upgrade,
                         db_trinket.details.infix_upgrade)

    def test_save_trinket(self):
        # given
        trinket = self._build_item()

        # when
        db_trinket = self.repository.save_trinket(trinket)

        # then
        self._assert_trinket(db_trinket, trinket)

    def test_get_trinket(self):
        # given
        trinket = self._build_item()
        self.repository.save_trinket(trinket)

        # when
        trinkets = self.repository.get_trinket()

        # then
        self.assertIsNotNone(trinkets)
        self.assertEqual(len(trinkets), 1)

        db_trinket = trinkets[0]
        self._assert_trinket(db_trinket, trinket)

    def test_get_trinket_by_type(self):
        # given
        trinket = self._build_item()
        self.repository.save_trinket(trinket)

        # when
        self.assertIsNone(
            self.repository.get_trinket(type=TrinketType.Ring))
        db_trinket = self.repository.get_trinket(type=TrinketType.Accessory)

        # then
        self._assert_trinket(db_trinket, trinket)

    def test_delete_trinkets(self):
        # given
        trinket = self._build_item()
        self.repository.save_trinket(trinket)

        # when
        self.repository.delete_trinket()
        db_trinket = self.repository.get_trinket()

        # then
        self.assertListEqual(db_trinket, [])

    def test_delete_trinket_by_type(self):
        # given
        trinket = self._build_item()
        self.repository.save_trinket(trinket)

        # when
        self.repository.delete_trinket(type=TrinketType.Accessory)
        db_trinket = self.repository.get_trinket()

        # then
        self.assertListEqual(db_trinket, [])
