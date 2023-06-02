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


class TestSpecializationsRepository(unittest.TestCase):

    data: Db = None
    repository: SpecializationsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = SpecializationsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build(self) -> Item:
        data = {
            'id': 1,
            'name': 'Test',
            'elite': True,
            'profession': '1',
            'icon': 'test',
            'background': 'test',
            'minor_traits': [3, 4],
            'major_traits': [1, 2]
        }

        return Specialization(data)

    def _assert(self, db_specialization: Specialization, specialization: Specialization):
        self.assertIsNotNone(db_specialization)
        self.assertEqual(specialization.id, db_specialization.id)
        self.assertEqual(specialization.name, db_specialization.name)
        self.assertEqual(specialization.elite, db_specialization.elite)
        self.assertListEqual(specialization.major_traits, [1, 2])
        self.assertListEqual(specialization.minor_traits, [3, 4])

    def test_save_specialization(self):
        # given
        specialization = self._build()

        # when
        db_specialization = self.repository.save_specialization(specialization)

        # then
        self._assert(db_specialization, specialization)

    def test_get_specializations(self):
        # given
        specialization = self._build()

        self.repository.save_specialization(specialization)

        # when
        db_specializations = self.repository.get_specializations()

        # then
        self.assertIsNotNone(db_specializations)
        self.assertEqual(len(db_specializations), 1)

        db_specialization = db_specializations[0]
        self._assert(db_specialization, specialization)

    def test_get_specialization_by_id(self):
        # given
        specialization = self._build()

        self.repository.save_specialization(specialization)

        # when
        self.assertIsNone(self.repository.get_specializations(id=2))
        db_specialization = self.repository.get_specializations(id=1)

        # then
        self._assert(db_specialization, specialization)

    def test_get_specialization_by_name(self):
        # given
        specialization = self._build()

        self.repository.save_specialization(specialization)

        # when
        self.assertListEqual(
            self.repository.get_specializations(name=specialization.name + 'abc'), [])
        db_specializations = self.repository.get_specializations(
            name=specialization.name)

        # then
        self.assertIsNotNone(db_specializations)
        self.assertEqual(len(db_specializations), 1)

        db_specialization = db_specializations[0]
        self._assert(db_specialization, specialization)

    def test_delete_specializations(self):
        # given
        specialization = self._build()

        self.repository.save_specialization(specialization)

        # when
        self.repository.delete_specializations()
        db_specializations = self.repository.get_specializations()

        # then
        self.assertListEqual(db_specializations, [])

    def test_delete_specialization_by_id(self):
        # given
        specialization = self._build()

        self.repository.save_specialization(specialization)

        # when
        self.repository.delete_specializations(id=1)
        db_specializations = self.repository.get_specializations()

        # then
        self.assertListEqual(db_specializations, [])
