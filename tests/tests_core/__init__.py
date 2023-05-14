#!/usr/bin/env python

import unittest

from .test_loader import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestLoader)
    return suite
