#!/usr/bin/env python

import unittest

from core import Loader
from core.loader import HEAVY_PROFESSIONS, LIGHT_PROFESSIONS, MEDIUM_PROFESSIONS
from model.api import Specialization

class TestLoader(unittest.TestCase):
    
    professions_dict: dict[str, list[str]] = {'Heavy': HEAVY_PROFESSIONS, 'Medium': MEDIUM_PROFESSIONS, 'Light': LIGHT_PROFESSIONS}
    
    num_specializations: int = 8
    
    loader: Loader = Loader()

    def test_load_professions(self):
        professions = self.loader.load_professions()
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