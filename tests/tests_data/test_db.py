#!/usr/bin/env python

import os
import shutil
import unittest
from unittest.mock import Mock

from config import ConfigProvider
from data import Db
from model.dao import *


curr_dir = os.path.dirname(os.path.abspath(__file__))
test_db_dir = os.path.join(curr_dir, 'tmp')
test_db_file = os.path.join(test_db_dir, 'data.fs')

class TestDb(unittest.TestCase):
    
    data: Db = None
        
    @classmethod
    def setUpClass(cls):
        unittest.TestCase.setUpClass()
        
        mockObject = ConfigProvider
        mockObject.get_data_dir = Mock(return_value=test_db_dir)
        mockObject.get_data_file = Mock(return_value=test_db_file)
        
        
    def setUp(self) -> None:
        super().setUp()
        self.data = Db()
        
    
    def tearDown(self) -> None:
        super().tearDown()
        del self.data
        shutil.rmtree(test_db_dir)
    
    
    def test_save_build(self):
        # given
        build = Build(1)
        
        # when
        db_build = self.data.save_build(build)
        
        # then       
        self.assertIsNotNone(db_build)
        self.assertEqual(build.build_number, db_build.build_number)
        self.assertIsNotNone(db_build.date)
        
    def test_delete_build(self):
        # given
        build = Build(1)
        self.data.save_build(build)
        db_build = self.data.get_build()
        self.assertIsNotNone(db_build)
        
        # when
        self.data.delete_build()
        db_build = self.data.get_build()
        
        # then       
        self.assertIsNone(db_build)

    def test_save_profession(self):
        # given
        profession = Profession(id=1, name='Test', code=1, icon='test', icon_big='big test')
        profession.add_flag('test flag')
        profession.add_specialization(1)
        profession.add_specialization(3)
        profession.add_specialization(1)
        
        weapon = Weapon('test', 1)
        profession.add_weapon(weapon)
        
        # when
        db_profession = self.data.save_profession(profession)
        
        # then       
        self.assertIsNotNone(db_profession)
        self.assertEqual(profession.id, db_profession.id)
        self.assertEqual(profession.name, db_profession.name)
        self.assertEqual(profession.code, db_profession.code)
        self.assertEqual(profession.icon, db_profession.icon)
        self.assertEqual(profession.icon_big, db_profession.icon_big)
        self.assertListEqual(profession.flags.data, ['test flag'])
        self.assertListEqual(profession.specializations.data, [1, 3])
        self.assertTrue(weapon in profession.weapons)
        
    def test_get_professions(self):
        # given
        profession = Profession(id=1, name='Test', code=1, icon='test', icon_big='big test')
        profession.add_flag('test flag')
        profession.add_specialization(1)
        profession.add_specialization(3)
        profession.add_specialization(1)
        
        weapon = Weapon('test', 1)
        profession.add_weapon(weapon)
        
        self.data.save_profession(profession)
        
        # when
        db_professions = self.data.get_professions()
        
        # then       
        self.assertIsNotNone(db_professions)
        self.assertEqual(len(db_professions), 1)
        
        db_profession = db_professions[0]
        self.assertEqual(profession.id, db_profession.id)
        self.assertEqual(profession.name, db_profession.name)
        self.assertEqual(profession.code, db_profession.code)
        self.assertEqual(profession.icon, db_profession.icon)
        self.assertEqual(profession.icon_big, db_profession.icon_big)
        self.assertListEqual(profession.flags.data, ['test flag'])
        self.assertListEqual(profession.specializations.data, [1, 3])
        self.assertTrue(weapon in profession.weapons)
        
    def test_get_profession_by_id(self):
        # given
        profession = Profession(id=1, name='Test', code=1, icon='test', icon_big='big test')
        profession.add_flag('test flag')
        profession.add_specialization(1)
        profession.add_specialization(3)
        profession.add_specialization(1)
        
        weapon = Weapon('test', 1)
        profession.add_weapon(weapon)
        
        self.data.save_profession(profession)
        
        # when
        self.assertIsNone(self.data.get_profession_by_id(2))
        db_profession = self.data.get_profession_by_id(1)
        
        # then       
        self.assertEqual(profession.id, db_profession.id)
        self.assertEqual(profession.name, db_profession.name)
        self.assertEqual(profession.code, db_profession.code)
        self.assertEqual(profession.icon, db_profession.icon)
        self.assertEqual(profession.icon_big, db_profession.icon_big)
        self.assertListEqual(profession.flags.data, ['test flag'])
        self.assertListEqual(profession.specializations.data, [1, 3])
        self.assertTrue(weapon in profession.weapons)
        
    def test_get_profession_by_name(self):
        # given
        profession = Profession(id=1, name='Test', code=1, icon='test', icon_big='big test')
        profession.add_flag('test flag')
        profession.add_specialization(1)
        profession.add_specialization(3)
        profession.add_specialization(1)
        
        weapon = Weapon('test', 1)
        profession.add_weapon(weapon)
        
        self.data.save_profession(profession)
        
        # when
        self.assertListEqual(self.data.get_profession_by_name('abc'), [])
        db_professions = self.data.get_profession_by_name('Test')
        
        # then       
        self.assertIsNotNone(db_professions)
        self.assertEqual(len(db_professions), 1)
        
        db_profession = db_professions[0]
        self.assertEqual(profession.id, db_profession.id)
        self.assertEqual(profession.name, db_profession.name)
        self.assertEqual(profession.code, db_profession.code)
        self.assertEqual(profession.icon, db_profession.icon)
        self.assertEqual(profession.icon_big, db_profession.icon_big)
        self.assertListEqual(profession.flags.data, ['test flag'])
        self.assertListEqual(profession.specializations.data, [1, 3])
        self.assertTrue(weapon in profession.weapons)
        
    def test_delete_professions(self):
        # given
        profession = Profession(id=1, name='Test', code=1, icon='test', icon_big='big test')
        profession.add_flag('test flag')
        profession.add_specialization(1)
        profession.add_specialization(3)
        profession.add_specialization(1)
        
        weapon = Weapon('test', 1)
        profession.add_weapon(weapon)
        
        self.data.save_profession(profession)
        
        # when
        self.data.delete_professions()
        db_professions = self.data.get_professions()
        
        # then       
        self.assertListEqual(db_professions, [])
        
    def test_delete_profession_by_id(self):
        # given
        profession = Profession(id=1, name='Test', code=1, icon='test', icon_big='big test')
        profession.add_flag('test flag')
        profession.add_specialization(1)
        profession.add_specialization(3)
        profession.add_specialization(1)
        
        weapon = Weapon('test', 1)
        profession.add_weapon(weapon)
        
        self.data.save_profession(profession)
        
        # when
        self.data.delete_profession_by_id(1)
        db_professions = self.data.get_professions()
        
        # then       
        self.assertListEqual(db_professions, [])
        
    def test_save_specialization(self):
        # given
        specialization = Specialization(id=1, name='Test', elite=True, profession=1, icon='test', background='test')
        specialization.add_major_trait(1)
        specialization.add_major_trait(2)
        specialization.add_minor_trait(3)
        specialization.add_minor_trait(4)
        
        # when
        db_specialization = self.data.save_specialization(specialization)
        
        # then       
        self.assertIsNotNone(db_specialization)
        self.assertEqual(specialization.id, db_specialization.id)
        self.assertEqual(specialization.name, db_specialization.name)
        self.assertEqual(specialization.elite, db_specialization.elite)
        self.assertListEqual(specialization.major_traits.data, [1, 2])
        self.assertListEqual(specialization.minor_traits.data, [3, 4])
        
    def test_get_specializations(self):
        # given
        specialization = Specialization(id=1, name='Test', elite=True, profession=1, icon='test', background='test')
        specialization.add_major_trait(1)
        specialization.add_major_trait(2)
        specialization.add_minor_trait(3)
        specialization.add_minor_trait(4)
        
        self.data.save_specialization(specialization)
        
        # when
        db_specializations = self.data.get_specializations()
        
        # then       
        self.assertIsNotNone(db_specializations)
        self.assertEqual(len(db_specializations), 1)
        
        db_specialization = db_specializations[0]
        self.assertIsNotNone(db_specialization)
        self.assertEqual(specialization.id, db_specialization.id)
        self.assertEqual(specialization.name, db_specialization.name)
        self.assertEqual(specialization.elite, db_specialization.elite)
        self.assertListEqual(specialization.major_traits.data, [1, 2])
        self.assertListEqual(specialization.minor_traits.data, [3, 4])
        
    def test_get_specialization_by_id(self):
        # given
        specialization = Specialization(id=1, name='Test', elite=True, profession=1, icon='test', background='test')
        specialization.add_major_trait(1)
        specialization.add_major_trait(2)
        specialization.add_minor_trait(3)
        specialization.add_minor_trait(4)
        
        self.data.save_specialization(specialization)
        
        # when
        self.assertIsNone(self.data.get_specialization_by_id(2))
        db_specialization = self.data.get_specialization_by_id(1)
        
         # then       
        self.assertIsNotNone(db_specialization)
        self.assertEqual(specialization.id, db_specialization.id)
        self.assertEqual(specialization.name, db_specialization.name)
        self.assertEqual(specialization.elite, db_specialization.elite)
        self.assertListEqual(specialization.major_traits.data, [1, 2])
        self.assertListEqual(specialization.minor_traits.data, [3, 4])
        
    def test_get_specialization_by_name(self):
        # given
        specialization = Specialization(id=1, name='Test', elite=True, profession=1, icon='test', background='test')
        specialization.add_major_trait(1)
        specialization.add_major_trait(2)
        specialization.add_minor_trait(3)
        specialization.add_minor_trait(4)
        
        self.data.save_specialization(specialization)
        
        # when
        self.assertListEqual(self.data.get_specialization_by_name('abc'), [])
        db_specializations = self.data.get_specialization_by_name('Test')
        
        # then       
        self.assertIsNotNone(db_specializations)
        self.assertEqual(len(db_specializations), 1)
        
        db_specialization = db_specializations[0]
        self.assertIsNotNone(db_specialization)
        self.assertEqual(specialization.id, db_specialization.id)
        self.assertEqual(specialization.name, db_specialization.name)
        self.assertEqual(specialization.elite, db_specialization.elite)
        self.assertListEqual(specialization.major_traits.data, [1, 2])
        self.assertListEqual(specialization.minor_traits.data, [3, 4])
        
    def test_delete_specializations(self):
        # given
        specialization = Specialization(id=1, name='Test', elite=True, profession=1, icon='test', background='test')
        specialization.add_major_trait(1)
        specialization.add_major_trait(2)
        specialization.add_minor_trait(3)
        specialization.add_minor_trait(4)
        
        self.data.save_specialization(specialization)
        
        # when
        self.data.delete_specializations()
        db_specializations = self.data.get_specializations()
        
        # then       
        self.assertListEqual(db_specializations, [])
        
    def test_delete_specialization_by_id(self):
        # given
        specialization = Specialization(id=1, name='Test', elite=True, profession=1, icon='test', background='test')
        specialization.add_major_trait(1)
        specialization.add_major_trait(2)
        specialization.add_minor_trait(3)
        specialization.add_minor_trait(4)
        
        self.data.save_specialization(specialization)
        
        # when
        self.data.delete_specialization_by_id(1)
        db_specializations = self.data.get_specializations()
        
        # then       
        self.assertListEqual(db_specializations, [])