#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model.dao import *
from model import ItemType


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestBuildRepository(unittest.TestCase):

    data: Db = None
    repository: ArmorRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = BuildRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_item(self) -> Item:
        kwargs = {}
        return Item(id=1, chat_link='[abcde1]', name='Tet', icon='test', description='test', type=ItemType.Armor, rarity=ItemRarity.Legendary)

    def test_save_armor(self):
        # given
        build = Item(1)

        # when
        db_build = self.repository.save_build(build)

        # then
        self.assertIsNotNone(db_build)
        self.assertEqual(build.build_number, db_build.build_number)
        self.assertIsNotNone(db_build.date)

    def test_delete_build(self):
        # given
        build = Build(1)
        self.repository.save_build(build)
        db_build = self.repository.get_build()
        self.assertIsNotNone(db_build)

        # when
        self.repository.delete_build()
        db_build = self.repository.get_build()

        # then
        self.assertIsNone(db_build)
