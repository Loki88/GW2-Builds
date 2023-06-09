#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model import ItemType, ItemRarity, InfusionFlag, UpgradeComponentFlags,\
    UpgradeComponentType, InfusionFlag, Item, Attribute


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestInfusionsRepository(unittest.TestCase):

    data: Db = None
    repository: InfusionRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = InfusionRepository()

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

    def _assert_infusion(self, db_infusion: Item, infusion: Item):
        self.assertIsNotNone(db_infusion)
        self.assertEqual(infusion.type, db_infusion.type)
        self.assertEqual(infusion.chat_link, db_infusion.chat_link)
        self.assertEqual(infusion.name, db_infusion.name)
        self.assertEqual(infusion.icon, db_infusion.icon)
        self.assertEqual(infusion.description, db_infusion.description)
        self.assertEqual(infusion.rarity, db_infusion.rarity)
        self.assertEqual(infusion.details.type, db_infusion.details.type)
        self.assertEqual(infusion.details.infix_upgrade.id,
                         db_infusion.details.infix_upgrade.id)
        self.assertListEqual(infusion.details.flags,
                             db_infusion.details.flags)
        self.assertListEqual(infusion.details.infusion_upgrade_flags,
                             db_infusion.details.infusion_upgrade_flags)

    def test_save_infusion(self):
        # given
        infusion = self._build_item()

        # when
        self.repository.save_infusion(infusion)

        # then
        self.assertIsNone(None, "Check that save does not throw")

    def test_get_infusion(self):
        # given
        infusion = self._build_item()
        self.repository.save_infusion(infusion)

        # when
        infusions = self.repository.get_infusion()

        # then
        self.assertIsNotNone(infusions)
        self.assertEqual(len(infusions), 1)

        db_infusion = infusions[0]
        self._assert_infusion(db_infusion, infusion)

    def test_get_infusion_by_id(self):
        # given
        infusion = self._build_item()
        self.repository.save_infusion(infusion)

        # when
        self.assertIsNone(
            self.repository.get_infusion(id=2))
        db_infusion = self.repository.get_infusion(id=1)

        # then
        self._assert_infusion(db_infusion, infusion)

    def test_delete_infusions(self):
        # given
        infusion = self._build_item()
        self.repository.save_infusion(infusion)

        # when
        self.repository.delete_infusion()
        db_infusion = self.repository.get_infusion()

        # then
        self.assertListEqual(db_infusion, [])

    def test_delete_infusion_by_type(self):
        # given
        infusion = self._build_item()
        self.repository.save_infusion(infusion)

        # when
        self.repository.delete_infusion(id=1)
        db_infusion = self.repository.get_infusion()

        # then
        self.assertListEqual(db_infusion, [])
