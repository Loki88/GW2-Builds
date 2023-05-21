#!/usr/bin/env python

import unittest

from config import ConfigProvider

class TestConfig(unittest.TestCase):
    
    config = ConfigProvider()
    
    def test_config(self):
        self.assertIsNotNone(self.config.get_data_folder())
        self.assertIsNotNone(self.config.get_folder())
        self.assertIsNotNone(self.config.get_parallel_limit())
        self.assertIsNotNone(self.config.get_path())
        