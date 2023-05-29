#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model.dao import *
from model import ItemType, ItemRarity, UpgradeComponentFlags, UpgradeComponentType, UpgradeComponentDetail, InfixBuff


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestRunesRepository(unittest.TestCase):

    data: Db = None
    repository: RunesRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = RunesRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_item(self) -> Item:
        infix_buff = InfixBuff(skill_id=14, description='Test')
        infix_bonus = [InfixAttributeBonus(
            Attribute.ConditionDamage, modifier=5)]
        infix_upgrade = InfixUpgrade(
            id=1, attributes=infix_bonus, buff=infix_buff)
        detail = UpgradeComponentDetail(
            type=UpgradeComponentType.Rune, infix_upgrade=infix_upgrade)
        detail.add_bonus('expertise')
        detail.add_flag(UpgradeComponentFlags.Weapons)
        return Item(id=1, chat_link='[abcde1]', name='Test', icon='test', description='test', type=ItemType.UpgradeComponent, rarity=ItemRarity.Legendary, details=detail)

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
        self.assertListEqual(rune.details.flags.data,
                             db_rune.details.flags.data)
        self.assertListEqual(rune.details.infusion_upgrade_flags.data,
                             db_rune.details.infusion_upgrade_flags.data)

    def test_save_rune(self):
        # given
        rune = self._build_item()

        # when
        db_rune = self.repository.save_rune(rune)

        # then
        self._assert_rune(db_rune, rune)

    def test_get_rune(self):
        # given
        rune = self._build_item()
        self.repository.save_rune(rune)

        # when
        runes = self.repository.get_rune()

        # then
        self.assertIsNotNone(runes)
        self.assertEqual(len(runes), 1)

        db_rune = runes[0]
        self._assert_rune(db_rune, rune)

    def test_get_rune_by_id(self):
        # given
        rune = self._build_item()
        self.repository.save_rune(rune)

        # when
        self.assertIsNone(
            self.repository.get_rune(id=2))
        db_rune = self.repository.get_rune(id=1)

        # then
        self._assert_rune(db_rune, rune)

    def test_delete_runes(self):
        # given
        rune = self._build_item()
        self.repository.save_rune(rune)

        # when
        self.repository.delete_rune()
        db_rune = self.repository.get_rune()

        # then
        self.assertListEqual(db_rune, [])

    def test_delete_rune_by_type(self):
        # given
        rune = self._build_item()
        self.repository.save_rune(rune)

        # when
        self.repository.delete_rune(id=1)
        db_rune = self.repository.get_rune()

        # then
        self.assertListEqual(db_rune, [])
