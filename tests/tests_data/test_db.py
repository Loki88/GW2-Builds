#!/usr/bin/env python

import unittest

from data import Db

class TestDb(unittest.TestCase):
    
    data = Db()
    
    def test_storage(self):
        self.assertIsNotNone(self.data.db)
        self.assertIsNotNone(self.data.db.database_name)