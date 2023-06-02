#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import *
from model import *


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')


class TestTraitRepository(unittest.TestCase):

    data: Db = None
    repository: TraitsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = TraitsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_trait(self) -> Trait:
        data = {
            'id': 1,
            'name': 'Test',
            'icon': 'test',
            'description': 'test desc',
            'specialization': 1,
            'tier': 2,
            'slot': TraitSlot.Major.name
        }
        return Trait(data)

    def _assert_trait(self, trait: Trait, db_trait: Trait):
        self.assertIsNotNone(db_trait)
        self.assertEqual(trait.name, db_trait.name)
        self.assertEqual(trait.icon, db_trait.icon)
        self.assertEqual(trait.description, db_trait.description)
        self.assertEqual(trait.specialization, db_trait.specialization)
        self.assertEqual(trait.tier, db_trait.tier)
        self.assertEqual(trait.slot, db_trait.slot)

    def test_save_trait(self):
        # given
        trait = self._build_trait()

        # when
        db_trait = self.repository.save_trait(trait)

        # then
        self._assert_trait(trait, db_trait)

    def test_get_traits(self):
        # given
        trait = self._build_trait()
        self.repository.save_trait(trait)

        # when
        db_traits = self.repository.get_trait()

        # then
        self.assertIsNotNone(db_traits)
        self.assertEqual(len(db_traits), 1)

        db_trait = db_traits[0]
        self._assert_trait(trait, db_trait)

    def test_get_trait_by_id(self):
        # given
        trait = self._build_trait()
        self.repository.save_trait(trait)

        # when
        self.assertIsNone(self.repository.get_trait(2))
        db_trait = self.repository.get_trait(1)

        # then
        self._assert_trait(trait, db_trait)

    def test_delete_traits(self):
        # given
        trait = self._build_trait()
        self.repository.save_trait(trait)

        # when
        self.repository.delete_trait()
        db_traits = self.repository.get_trait()

        # then
        self.assertListEqual(db_traits, [])

    def test_delete_trait_by_id(self):
        # given
        trait = self._build_trait()
        self.repository.save_trait(trait)

        # when
        self.repository.delete_trait(1)
        db_traits = self.repository.get_trait()

        # then
        self.assertListEqual(db_traits, [])
