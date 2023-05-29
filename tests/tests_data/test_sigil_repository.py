#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model.dao import *
from model import ItemType, InfusionFlag, UpgradeComponentFlags, UpgradeComponentType, UpgradeComponentDetail, InfixBuff


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestInfusionsRepository(unittest.TestCase):

    data: Db = None
    repository: SigilsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = SigilsRepository()

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
            type=UpgradeComponentType.Sigil, infix_upgrade=infix_upgrade)
        detail.add_bonus('expertise')
        detail.add_flag(UpgradeComponentFlags.Weapons)
        return Item(id=1, chat_link='[abcde1]', name='Tet', icon='test', description='test', type=ItemType.UpgradeComponent, rarity=ItemRarity.Legendary, details=detail)

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
        self.assertListEqual(sigil.details.flags.data,
                             db_sigil.details.flags.data)
        self.assertListEqual(sigil.details.infusion_upgrade_flags.data,
                             db_sigil.details.infusion_upgrade_flags.data)

    def test_save_sigil(self):
        # given
        sigil = self._build_item()

        # when
        db_sigil = self.repository.save_sigil(sigil)

        # then
        self._assert_sigil(db_sigil, sigil)

    def test_get_sigil(self):
        # given
        sigil = self._build_item()
        self.repository.save_sigil(sigil)

        # when
        sigils = self.repository.get_sigil()

        # then
        self.assertIsNotNone(sigils)
        self.assertEqual(len(sigils), 1)

        db_sigil = sigils[0]
        self._assert_sigil(db_sigil, sigil)

    def test_get_sigil_by_id(self):
        # given
        sigil = self._build_item()
        self.repository.save_sigil(sigil)

        # when
        self.assertIsNone(
            self.repository.get_sigil(id=2))
        db_sigil = self.repository.get_sigil(id=1)

        # then
        self._assert_sigil(db_sigil, sigil)

    def test_delete_sigils(self):
        # given
        sigil = self._build_item()
        self.repository.save_sigil(sigil)

        # when
        self.repository.delete_sigil()
        db_sigil = self.repository.get_sigil()

        # then
        self.assertListEqual(db_sigil, [])

    def test_delete_sigil_by_type(self):
        # given
        sigil = self._build_item()
        self.repository.save_sigil(sigil)

        # when
        self.repository.delete_sigil(id=1)
        db_sigil = self.repository.get_sigil()

        # then
        self.assertListEqual(db_sigil, [])
