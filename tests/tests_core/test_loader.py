#!/usr/bin/env python

import unittest

from core import Loader
from core.loader import HEAVY_PROFESSIONS, LIGHT_PROFESSIONS, MEDIUM_PROFESSIONS

class TestLoader(unittest.TestCase):
    
    professions_dict: dict[str, list[str]] = {'Heavy': HEAVY_PROFESSIONS, 'Medium': MEDIUM_PROFESSIONS, 'Light': LIGHT_PROFESSIONS}
    
    num_specializations: int = 8

    def test_load_professions(self):
        loader = Loader()
        professions = loader.load_professions()
        self.assertIsNotNone(professions)
        self.assertEqual(len(professions), 9)

    def test_load_specializations(self):
        loader = Loader()
        for profession_type, professions_ids in self.professions_dict.items():
            professions = loader.load_professions(professions_ids)
            self.assertIsNotNone(professions)
            self.assertEqual(len(professions), len(professions_ids))
            
            specializations = loader.load_specializations(professions)
            self.assertIsNotNone(specializations)
            self.assertEqual(len(specializations), len(professions_ids)*self.num_specializations)