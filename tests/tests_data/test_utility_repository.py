#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model.dao import *
from model import ItemType, ItemRarity, ConsumableType

curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestInfusionsRepository(unittest.TestCase):

    data: Db = None
    repository: UtilitiesRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = UtilitiesRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_item(self) -> Item:
        detail = ConsumableDetail(type=ConsumableType.Utility, description="abc",
                                  duration_ms=30000, recipe_id=1, apply_count=1, name='Test', icon='test')
        return Item(id=1, chat_link='[abcde1]', name='Tet', icon='test', description='test', type=ItemType.Consumable, rarity=ItemRarity.Ascended, details=detail)

    def _assert_utility(self, db_utility: Item, utility: Item):
        self.assertIsNotNone(db_utility)
        self.assertEqual(utility.type, db_utility.type)
        self.assertEqual(utility.chat_link, db_utility.chat_link)
        self.assertEqual(utility.name, db_utility.name)
        self.assertEqual(utility.icon, db_utility.icon)
        self.assertEqual(utility.description, db_utility.description)
        self.assertEqual(utility.rarity, db_utility.rarity)
        self.assertEqual(utility.details.type, db_utility.details.type)
        self.assertEqual(utility.details.type,
                         db_utility.details.type)
        self.assertEqual(utility.details.description,
                         db_utility.details.description)
        self.assertEqual(utility.details.duration_ms,
                         db_utility.details.duration_ms)
        self.assertEqual(utility.details.recipe_id,
                         db_utility.details.recipe_id)
        self.assertEqual(utility.details.apply_count,
                         db_utility.details.apply_count)
        self.assertEqual(utility.details.name,
                         db_utility.details.name)
        self.assertEqual(utility.details.icon,
                         db_utility.details.icon)

    def test_save_utility(self):
        # given
        utility = self._build_item()

        # when
        db_utility = self.repository.save_utility(utility)

        # then
        self._assert_utility(db_utility, utility)

    def test_get_utility(self):
        # given
        utility = self._build_item()
        self.repository.save_utility(utility)

        # when
        utilitys = self.repository.get_utility()

        # then
        self.assertIsNotNone(utilitys)
        self.assertEqual(len(utilitys), 1)

        db_utility = utilitys[0]
        self._assert_utility(db_utility, utility)

    def test_get_utility_by_id(self):
        # given
        utility = self._build_item()
        self.repository.save_utility(utility)

        # when
        self.assertIsNone(
            self.repository.get_utility(id=2))
        db_utility = self.repository.get_utility(id=1)

        # then
        self._assert_utility(db_utility, utility)

    def test_delete_utilitys(self):
        # given
        utility = self._build_item()
        self.repository.save_utility(utility)

        # when
        self.repository.delete_utility()
        db_utility = self.repository.get_utility()

        # then
        self.assertListEqual(db_utility, [])

    def test_delete_utility_by_type(self):
        # given
        utility = self._build_item()
        self.repository.save_utility(utility)

        # when
        self.repository.delete_utility(id=1)
        db_utility = self.repository.get_utility()

        # then
        self.assertListEqual(db_utility, [])
