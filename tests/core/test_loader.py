#!/usr/bin/env python

import unittest

from core.loader import Loader

class TestLoader(unittest.TestCase):

    def test_load_professions(self):
        loader = Loader()
        professions = loader.load_professions()
        self.assertIsNotNone(professions)
        self.assertEqual(len(professions), 9)

    
