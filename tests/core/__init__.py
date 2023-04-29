#!/usr/bin/env python

import sys
import unittest

from .test_loader import *

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestLoader)
    return suite

if __name__ == '__main__':
    unittest.main(sys.modules[__name__])