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


class TestStatsRepository(unittest.TestCase):

    data: Db = None
    repository: StatsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = StatsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build(self) -> ItemStats:
        data = {
            'id': 1,
            'name': 'Test',
            'attributes': [
                {
                    'attribute': Attribute.AgonyResistance.name,
                    'multiplier': 5,
                    'value': 3
                }
            ]
        }

        return ItemStats(data)

    def _assert(self, db_stats: ItemStats, stats: ItemStats):
        self.assertIsNotNone(db_stats)
        self.assertEqual(stats.id, db_stats.id)
        self.assertEqual(stats.name, db_stats.name)
        self.assertListEqual([(x.attribute, x.multiplier, x.value) for x in stats.attributes],
                             [(x.attribute, x.multiplier, x.value) for x in db_stats.attributes])

    def test_save_stat(self):
        # given
        stats = self._build()

        # when
        self.repository.save_stat(stats)

        # then
        self.assertIsNone(None, "Check that save does not throw")

    def test_get_stats(self):
        # given
        stats = self._build()

        self.repository.save_stat(stats)

        # when
        db_stats = self.repository.get_stats()

        # then
        self.assertIsNotNone(db_stats)
        self.assertEqual(len(db_stats), 1)

        db_stat = db_stats[0]
        self._assert(db_stat, stats)

    def test_get_stat_by_id(self):
        # given
        stats = self._build()

        self.repository.save_stat(stats)

        # when
        self.assertIsNone(self.repository.get_stats(id=2))
        db_stat = self.repository.get_stats(id=1)

        # then
        self._assert(db_stat, stats)

    def test_get_stat_by_name(self):
        # given
        stats = self._build()

        self.repository.save_stat(stats)

        # when
        self.assertListEqual(
            self.repository.get_stats(name=stats.name + 'abc'), [])
        db_stats = self.repository.get_stats(
            name=stats.name)

        # then
        self.assertIsNotNone(db_stats)
        self.assertEqual(len(db_stats), 1)

        db_stat = db_stats[0]
        self._assert(db_stat, stats)

    def test_delete_stats(self):
        # given
        stats = self._build()

        self.repository.save_stat(stats)

        # when
        self.repository.delete_stats()
        db_stats = self.repository.get_stats()

        # then
        self.assertListEqual(db_stats, [])

    def test_delete_stat_by_id(self):
        # given
        stats = self._build()

        self.repository.save_stat(stats)

        # when
        self.repository.delete_stats(id=1)
        db_stats = self.repository.get_stats()

        # then
        self.assertListEqual(db_stats, [])
