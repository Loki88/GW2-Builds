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


class TestProfessionsRepository(unittest.TestCase):

    data: Db = None
    repository: ProfessionsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mock_object = ConfigProvider
        mock_object.get_data_dir = Mock(return_value=test_db_dir)
        mock_object.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = ProfessionsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build_profession(self) -> Profession:
        data = {
            'id': 1,
            'name': 'Test',
            'code': 1,
            'icon': 'test',
            'icon_big': 'big test',
            'flags': ['test flag'],
            'specializations': [1, 3, 1],
            'weapons': {
                'test': {
                    'name': 'abc',
                    'specialization': 3,
                    'skills': [
                        {
                            'id': 2,
                            'slot': 1
                        }
                    ]
                }
            }
        }
        return Profession(data)

    def _assert_profession(self, profession: Profession, db_profession: Profession):
        self.assertIsNotNone(db_profession)
        self.assertEqual(profession.id, db_profession.id)
        self.assertEqual(profession.name, db_profession.name)
        self.assertEqual(profession.code, db_profession.code)
        self.assertEqual(profession.icon, db_profession.icon)
        self.assertEqual(profession.icon_big, db_profession.icon_big)
        self.assertListEqual(profession.flags, ['test flag'])
        self.assertListEqual(profession.specializations, [1, 3])
        self.assertListEqual([(x.name, x.specialization) for x in profession.weapons], [
                             (x.name, x.specialization) for x in db_profession.weapons])

    def test_save_profession(self):
        # given
        profession = self._build_profession()

        # when
        self.repository.save_profession(profession)

    def test_get_professions(self):
        # given
        profession = self._build_profession()

        self.repository.save_profession(profession)

        # when
        db_professions = self.repository.get_professions()

        # then
        self.assertIsNotNone(db_professions)
        self.assertEqual(len(db_professions), 1)

        db_profession = db_professions[0]
        self._assert_profession(profession, db_profession)

    def test_get_profession_by_id(self):
        # given
        profession = self._build_profession()

        self.repository.save_profession(profession)

        # when
        self.assertIsNone(self.repository.get_professions(id=2))
        db_profession = self.repository.get_professions(id=1)

        # then
        self._assert_profession(profession, db_profession)

    def test_get_profession_by_name(self):
        # given
        profession = self._build_profession()

        self.repository.save_profession(profession)

        # when
        self.assertListEqual(self.repository.get_professions(name='abc'), [])
        db_professions = self.repository.get_professions(name='Test')

        # then
        self.assertIsNotNone(db_professions)
        self.assertEqual(len(db_professions), 1)

        db_profession = db_professions[0]
        self._assert_profession(profession, db_profession)

    def test_delete_professions(self):
        # given
        profession = self._build_profession()

        self.repository.save_profession(profession)

        # when
        self.repository.delete_professions()
        db_professions = self.repository.get_professions()

        # then
        self.assertListEqual(db_professions, [])

    def test_delete_profession_by_id(self):
        # given
        profession = self._build_profession()

        self.repository.save_profession(profession)

        # when
        self.repository.delete_professions(id=1)
        db_professions = self.repository.get_professions()

        # then
        self.assertListEqual(db_professions, [])
