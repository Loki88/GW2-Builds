#!/usr/bin/env python

import unittest

from core import Loader
from core.loader import HEAVY_PROFESSIONS, LIGHT_PROFESSIONS, MEDIUM_PROFESSIONS
from model.api import Specialization

class TestLoader(unittest.TestCase):
    
    professions_dict: dict[str, list[str]] = {'Heavy': HEAVY_PROFESSIONS, 'Medium': MEDIUM_PROFESSIONS, 'Light': LIGHT_PROFESSIONS}
    
    num_specializations: int = 8
    
    loader: Loader = Loader()
    
    def test_load_build_id(self):
        # when
        build_id = self.loader.load_build_id();
        
        # then
        self.assertIsNotNone(build_id)

    def test_load_professions(self):
        # when
        professions = self.loader.load_professions()
        
        # then
        self.assertIsNotNone(professions)
        self.assertEqual(len(professions), 9)

    def test_load_specializations(self):
        for profession_type, professions_ids in self.professions_dict.items():
            professions = self.loader.load_professions(professions_ids)
            self.assertIsNotNone(professions)
            self.assertEqual(len(professions), len(professions_ids))
            
            
            specializations = self.loader.load_specializations(professions)
            self.assertIsNotNone(specializations)
            self.assertEqual(len(specializations), len(professions_ids)*self.num_specializations)
            
    def test_load_traits(self):
        # given
        specializations = [
            Specialization({'id': 1, 'minor_traits': [214, 265], 'major_traits': [265]}),
            Specialization({'id': 2, 'minor_traits': [265], 'major_traits': [214, 265]}),
        ]
        
        # when
        traits = self.loader.load_traits(specializations)
        
        # then
        self.assertIsNotNone(traits)
        self.assertEqual(len(traits), 2)
        self.assertListEqual([x.id for x in traits], [214, 265])
        
    def test_load_skills(self):
        # given
        skills_ids = [1110, 1115, 1118, 1123, 1125, 1129, 1131, 1139, 1141, 1148, 1162, 1167, 1175, 1279, 1355, 1359, 1364, 1408]
        
        # when
        skills = self.loader.load_skills(skills_ids)
        
        # then
        self.assertIsNotNone(skills)
        self.assertEqual(len(skills), len(skills_ids))
        self.assertListEqual([x.id for x in skills], skills_ids)
        
