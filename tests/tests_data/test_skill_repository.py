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


class TestSkillsRepository(unittest.TestCase):

    data: Db = None
    repository: SkillsRepository = None

    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()

        mock_object = ConfigProvider
        mock_object.get_data_dir = Mock(return_value=test_db_dir)
        mock_object.get_data_file = Mock(return_value=test_db_file)

    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        self.repository = SkillsRepository()

    def tearDown(self) -> None:
        super().tearDown()
        del self.repository
        del self.data
        shutil.rmtree(test_db_dir)

    def _build(self) -> Skill:
        data = {
            'name': 'Conjure Fiery Greatsword',
            'description': 'Conjure. Manifest a fiery greatsword..',
            'type': 'Elite',
            'weapon_type': 'None',
            'professions': [
                'Elementalist'
            ],
            'slot': 'Elite',
            'categories': [
                'Conjure'
            ],
            'bundle_skills': [2, 3, 4, 5, 6],
            'icon': '..',
            'id': 1
        }

        return Skill(data)

    def _assert(self, db_skills: Skill, skills: Skill):
        self.assertIsNotNone(db_skills)
        self.assertEqual(skills.id, db_skills.id)
        self.assertEqual(skills.name, db_skills.name)
        self.assertEqual(skills.description, db_skills.description)
        self.assertEqual(skills.type, db_skills.type)
        self.assertEqual(skills.slot, db_skills.slot)
        self.assertEqual(skills.icon, db_skills.icon)
        self.assertListEqual(skills.professions, db_skills.professions)
        self.assertListEqual(skills.bundle_skills, db_skills.bundle_skills)
        self.assertListEqual(skills.categories, db_skills.categories)

    def test_save_skill(self):
        # given
        skills = self._build()

        # when
        self.repository.save_skill(skills)

        # then
        self.assertIsNone(None, 'Check that save does not throw')

    def test_get_skills(self):
        # given
        skills = self._build()

        self.repository.save_skill(skills)

        # when
        db_skills = self.repository.get_skills()

        # then
        self.assertIsNotNone(db_skills)
        self.assertEqual(len(db_skills), 1)

        db_skill = db_skills[0]
        self._assert(db_skill, skills)

    def test_get_skill_by_id(self):
        # given
        skills = self._build()

        self.repository.save_skill(skills)

        # when
        self.assertIsNone(self.repository.get_skills(id=2))
        db_skill = self.repository.get_skills(id=1)

        # then
        self._assert(db_skill, skills)

    def test_get_skill_by_name(self):
        # given
        skills = self._build()

        self.repository.save_skill(skills)

        # when
        self.assertListEqual(
            self.repository.get_skills(name=skills.name + 'abc'), [])
        db_skills = self.repository.get_skills(
            name=skills.name)

        # then
        self.assertIsNotNone(db_skills)
        self.assertEqual(len(db_skills), 1)

        db_skill = db_skills[0]
        self._assert(db_skill, skills)

    def test_delete_skills(self):
        # given
        skills = self._build()

        self.repository.save_skill(skills)

        # when
        self.repository.delete_skills()
        db_skills = self.repository.get_skills()

        # then
        self.assertListEqual(db_skills, [])

    def test_delete_skill_by_id(self):
        # given
        skills = self._build()

        self.repository.save_skill(skills)

        # when
        self.repository.delete_skills(id=1)
        db_skills = self.repository.get_skills()

        # then
        self.assertListEqual(db_skills, [])
